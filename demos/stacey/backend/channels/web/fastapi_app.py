# channels/web/fastapi_app.py
import json
import traceback

import uvicorn
from fastapi import FastAPI, Request, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

from channels.web.web_communication_channel import WebCommunicationChannel
from media.media_replace import replace_media_prompt_with_media_url_formatted_as_markdown, MediaGenerator


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        print("connect socket")
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        print("disconnect socket")
        self.active_connections.remove(websocket)

    async def send_message(self, event_type: str, message: dict):
        formatted_message = {
            "eventType": event_type,
            "data": message
        }
        closed_connections = []  # List to hold closed connections for later removal
        for connection in self.active_connections:
            # noinspection PyBroadException
            try:
                print("Sending message to socket")
                await connection.send_text(json.dumps(formatted_message))
                print("Successfully sent message to socket")
            except Exception:
                print("Socket not open, marking for removal from active connections")
                closed_connections.append(connection)  # Mark closed connections for removal

        # Remove closed connections from active_connections list
        for closed_connection in closed_connections:
            self.active_connections.remove(closed_connection)


class FastApiApp:
    def __init__(self, ace_system, media_generators: [MediaGenerator]):
        self.app = FastAPI()
        self.ace = ace_system
        self.media_generators = media_generators
        self.connection_manager = ConnectionManager()
        self.app.add_exception_handler(Exception, self.custom_exception_handler)

        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.setup_routes()

    # noinspection PyUnusedLocal
    async def custom_exception_handler(self, request: Request, exc: Exception):
        """
        Custom exception handler that logs the stack trace and returns a JSON response.
        """
        print("custom_exception_handler called")
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(content={"error": str(exc), "traceback": traceback_str}, status_code=500)

    def setup_routes(self):
        app = self.app  # to shorten the code

        @app.websocket("/ws/")
        async def websocket_endpoint(websocket: WebSocket):
            print("websocket_endpoint called")
            await self.connection_manager.connect(websocket)
            print("2")

        # noinspection PyUnusedLocal
        @app.exception_handler(Exception)
        async def custom_exception_handler(request: Request, exc: Exception):
            """
            Custom exception handler that logs the stack trace and returns a JSON response.
            """
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JSONResponse(content={"error": str(exc), "traceback": traceback_str}, status_code=500)

        @app.post("/chat/")
        async def chat(request: Request):
            data = await request.json()
            conversation = data.get('conversation', [])
            communication_channel = WebCommunicationChannel(conversation)

            try:
                await self.ace.l3_agent.process_incoming_user_message(communication_channel)
                if communication_channel.response is None:
                    print("No response from process_incoming_user_message")
                    return {"role": "assistant", "name": "Stacey", "content": "(no response)"}
                print("process_incoming_user_message completed. Response: " + communication_channel.response)
                response_with_images = await replace_media_prompt_with_media_url_formatted_as_markdown(
                    self.media_generators, communication_channel.response
                )
                return {"role": "assistant", "name": "Stacey", "content": response_with_images}
            except Exception as e:
                traceback_str = traceback.format_exc()
                print(traceback_str)
                return JSONResponse(content={"error": str(e), "traceback": traceback_str}, status_code=400)

        @app.get("/chat/")
        async def chat_get(message: str):
            """
            For testing purposes. Lets you send a single chat message (without a conversation history)
            and see the raw response from GPT.
            """
            if not message:
                raise HTTPException(status_code=400, detail="message parameter is required")
            conversation = [{"role": "user", "name": "web-user", "content": message}]
            communication_channel = WebCommunicationChannel(conversation)

            try:
                await self.ace.l3_agent.process_incoming_user_message(communication_channel)
                if communication_channel.response is None:
                    print("No response from ask_llm_which_actions_to_take")
                    return "(no response)"
                return communication_channel.response
            except Exception as e:
                traceback_str = traceback.format_exc()
                print(traceback_str)
                return JSONResponse(content={"error": str(e), "traceback": traceback_str}, status_code=400)

        @app.get("/bus/")
        async def view_bus(name: str):
            if name == 'northbound':
                return self.ace.northbound_bus.messages()
            elif name == 'southbound':
                return self.ace.southbound_bus.messages()
            else:
                raise HTTPException(status_code=400, detail="Invalid bus name. Choose 'northbound' or 'southbound'.")

        @app.post("/publish_message/")
        async def publish_message(request: Request):
            print("publish_message called")
            data = await request.json()
            print("data: " + str(data))
            sender = data.get('sender')
            message = data.get('message')
            bus_name = data.get('bus')

            if not sender or not message or not bus_name:
                print("sender, message, and bus are required fields")
                raise HTTPException(status_code=400, detail="sender, message, and bus are required fields")

            if bus_name == 'northbound':
                bus = self.ace.northbound_bus
            elif bus_name == 'southbound':
                bus = self.ace.southbound_bus
            else:
                raise HTTPException(status_code=400, detail="Invalid bus name. Choose 'northbound' or 'southbound'.")

            await bus.publish(sender, message)
            return {"success": True, "message": "Message published successfully"}

        @app.post("/clear_messages/")
        async def clear_messages(request: Request):
            data = await request.json()
            bus_name = data.get('bus')
            if not bus_name:
                raise HTTPException(status_code=400, detail="'bus' is a required field")

            if bus_name == 'northbound':
                bus = self.ace.northbound_bus
            elif bus_name == 'southbound':
                bus = self.ace.southbound_bus
            else:
                raise HTTPException(status_code=400, detail="Invalid bus name. Choose 'northbound' or 'southbound'.")

            bus.clear_messages()
            return {"success": True, "message": "Messages cleared successfully"}

        @app.get("/", response_class=HTMLResponse)
        def root():
            return ('<html>Hi! Stacey here. Yes, the backend is up and running! '
                    '<a href="chat?message=hi">/chat?message=hi</a></html>')

    def setup_listeners(self):
        for bus in [self.ace.northbound_bus, self.ace.southbound_bus]:
            bus.subscribe(self.create_bus_listener(bus))

        for layer in self.ace.get_layers():
            layer.add_status_listener(self.create_layer_status_listener(layer))

    def create_bus_listener(self, bus):
        async def listener(sender, message):
            try:
                print(f"flask_app detected message on bus from {sender}: {message}")
                event_type = f'bus-message'
                await self.connection_manager.send_message(event_type, {
                    'bus': bus.name,
                    'sender': sender,
                    'message': message
                })
            except Exception as e:
                print(f"Error in bus listener: {e}")
        return listener

    def create_layer_status_listener(self, layer):
        async def listener(status):
            try:
                print(f"flask_app detected status change in layer {layer.get_id}: {status}")
                event_type = f'layer-status'
                await self.connection_manager.send_message(event_type, {
                    'layerId': layer.get_id(),
                    'status': status.name
                })
            except Exception as e:
                print(f"Error in layer status listener: {e}")
        return listener

    async def run(self):
        self.setup_listeners()
        config = uvicorn.Config(app=self.app, host="localhost", port=5000)
        server = uvicorn.Server(config)
        await server.serve()

