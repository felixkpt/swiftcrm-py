from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from app.websocket.websocket_manager import WebSocketManager
from typing import Dict

router = APIRouter()

manager = WebSocketManager()

# Dictionary to store WebSocket connections with client_id
connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/notifications/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    
    await manager.connect(websocket)
    connections[client_id] = websocket  # Store the connection with client_id

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message({'messsage': f"You wrote: {data}"}, websocket)
            await manager.broadcast({'messsage': f"Client #{client_id} says: {data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

websocket_routes = router  # Export the router instance
