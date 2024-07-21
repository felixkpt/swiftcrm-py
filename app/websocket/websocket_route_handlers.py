# handlers/websocket_handlers.py
from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from app.websocket.websocket_manager import WebSocketManager
from typing import List

router = APIRouter()

manager = WebSocketManager()

connections: List[WebSocket] = []

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")

websocket_routes = router  # Export the router instance
