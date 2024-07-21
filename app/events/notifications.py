# events/notifications.py
from app.websocket.websocket_route_handlers import connections
from app.repositories.auto_page_builder_repo import AutoPageBuilder

class NotificationService:
    async def notify_model_updated(self, db, table_name: str, message: str):
        model_id = AutoPageBuilder.get_page_by_table_name(db, table_name).id
        # Notify WebSocket clients
        print(connections)
        for connection in connections:
            await connection.send_json({
                "model_id": model_id,
                "message": message,
            })
