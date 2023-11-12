import json

from starlette.websockets import WebSocket


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        print("connect socket")
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        print("disconnect socket")
        self.active_connections.remove(websocket)

    async def send_message(self, message):
        closed_connections = []
        for connection in self.active_connections:
            try:
                print("Sending message to socket")
                await connection.send_text(json.dumps(message))
                print("Successfully sent message to socket")
            except Exception:
                print("Socket not open, marking for removal from active connections")
                closed_connections.append(connection)
        for closed_connection in closed_connections:
            self.active_connections.remove(closed_connection)