from app.websocket.websocket_route_handlers import connections
from app.repositories.auto_page_builder.auto_page_builder_repo import AutoPageBuilderRepo

class NotificationService:
    async def notify_model_updated(self, db, table_name: str, message: str):
        model_id = AutoPageBuilderRepo.get_page_by_table_name_plural(db, table_name).name_plural
        # Notify WebSocket clients
        print(connections)
        for client_id, connection in connections.items():
            print(f"Notifying client {client_id} with connection {connection}")
            try:
                await connection.send_json({
                    "client_id": client_id,
                    "model_id": model_id,
                    "message": message,
                })
                print(f'Notified user: {client_id}')
            except Exception as e:
                print(f'NotificationService Error: {e}')
