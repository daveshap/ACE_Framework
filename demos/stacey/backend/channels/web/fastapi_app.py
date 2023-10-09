# channels/web/fastapi_app.py
import traceback

import uvicorn
from fastapi import FastAPI, Request, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

from ace.types import ChatMessage, create_chat_message, LayerState
from channels.web.web_communication_channel import WebCommunicationChannel
from channels.web.web_socket_connection_manager import WebSocketConnectionManager
from media.media_replace import MediaGenerator


class FastApiApp:
    def __init__(self, ace_system, media_generators: [MediaGenerator]):
        self.app = FastAPI()
        self.ace = ace_system
        self.media_generators = media_generators
        self.layer_connection_managers = {
            layer.get_id(): WebSocketConnectionManager() for layer in ace_system.get_layers()
        }
        self.bus_connection_managers = {
            'northbound': WebSocketConnectionManager(),
            'southbound': WebSocketConnectionManager()
        }
        self.chatConnectionManager = WebSocketConnectionManager()
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
        app = self.app

        @app.websocket("/ws-layer/{layer_id}/")
        async def websocket_endpoint_layer(websocket: WebSocket, layer_id: str):
            if layer_id not in self.layer_connection_managers:
                raise HTTPException(status_code=404, detail="Layer not found")
            print(f"websocket_endpoint_layer for {layer_id} called")
            await self.layer_connection_managers[layer_id].connect(websocket)

        @app.websocket("/ws-bus/{bus_name}/")
        async def websocket_endpoint_bus(websocket: WebSocket, bus_name: str):
            print("Blaj")
            if bus_name not in self.bus_connection_managers:
                print(f"Bus not found: {bus_name}")
                raise HTTPException(status_code=404, detail="Bus not found")
            print(f"websocket_endpoint_bus for {bus_name} called")
            await self.bus_connection_managers[bus_name].connect(websocket)

        @app.websocket("/ws-chat/")
        async def websocket_endpoint_chat(websocket: WebSocket):
            print("websocket_endpoint_chat called")
            await self.chatConnectionManager.connect(websocket)

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
            messages: [ChatMessage] = data.get('messages', [])
            communication_channel = WebCommunicationChannel(messages, self.chatConnectionManager, self.media_generators)

            try:
                await self.ace.l3_agent.process_incoming_user_message(communication_channel)
                return JSONResponse(content={"success": True}, status_code=200)
            except Exception as e:
                print("Damn, something went wrong while processing incoming user message!")
                traceback_str = traceback.format_exc()
                print(traceback_str)
                return create_chat_message("Stacey", f"Damn! Something went wrong: {str(e)}")

        @app.get("/chat/")
        async def chat_get(message: str):
            """
            For testing purposes. Lets you send a single chat message and see the response (if any)
            """
            if not message:
                raise HTTPException(status_code=400, detail="message parameter is required")
            messages = [create_chat_message("api-user", message)]
            communication_channel = WebCommunicationChannel(messages, self.chatConnectionManager, self.media_generators)

            try:
                await self.ace.l3_agent.process_incoming_user_message(communication_channel)
                return "Message sent to Stacey"
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

        @app.get("/layer_state/{layer_id}/")
        async def get_layer_state(layer_id: str):
            if layer_id not in self.layer_connection_managers:
                raise HTTPException(status_code=404, detail="Layer not found")
            layer = self.ace.get_layer(layer_id)
            if not layer:
                raise HTTPException(status_code=404, detail="Layer not found: " + layer_id)

            layer_state: LayerState = layer.get_layer_state()  # assuming get_current_state() is a method
            return layer_state

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
            layer.add_layer_state_listener(self.create_layer_state_listener(layer))

    def create_bus_listener(self, bus):
        async def listener(sender, message):
            try:
                print(f"flask_app detected message on {bus.name} from {sender}: {message}")
                await self.bus_connection_managers[bus.name].send_message({
                    'eventType': 'busMessage',
                    'data': {
                        'bus': bus.name,
                        'sender': sender,
                        'message': message
                    }
                })
            except Exception as e:
                print(f"Error in bus listener: {e}")
        return listener

    def create_layer_state_listener(self, layer):
        async def listener(layer_state: LayerState):
            try:
                print(f"flask_app detected state change in layer {layer.get_id()}: {layer_state}")
                await self.layer_connection_managers[layer.get_id()].send_message(layer_state)
            except Exception as e:
                print(f"Error in layer status listener: {e}")
        return listener

    async def run(self):
        self.setup_listeners()
        config = uvicorn.Config(app=self.app, host="localhost", port=5000)
        server = uvicorn.Server(config)
        return await server.serve()
