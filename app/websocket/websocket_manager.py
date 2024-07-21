from fastapi import WebSocket
from uuid import uuid4


class WebSocketManager:
    """
    Manage WebSocket connections and broadcast messages.
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        client_id = str(uuid4())
        await websocket.accept()
        self.active_connections.append(websocket)
        return client_id

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)
