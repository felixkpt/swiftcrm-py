# events/notifications.py
from app.websocket.websocket_route_handlers import connections


class NotificationService:
    async def notify_model_updated(self, model_id: str, message: str):
        # Notify WebSocket clients
        print(connections)
        for connection in connections:
            await connection.send_json({
                "model_id": model_id,
                "message": message,
            })
