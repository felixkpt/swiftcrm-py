from app.websocket.websocket_route_handlers import connections

class NotificationService:
    async def notify_model_updated(self, db, tableName: str, message: str):
        from app.modules.auto_builders.model_builder.model_builder_repo import ModelBuilderRepo
        res = ModelBuilderRepo.get_page_by_tableNamePlural(db, tableName)
        if res and res.createFrontendViews == 1:
            model_id = res.uuid
            model_name = res.nameSingular
            # Notify WebSocket clients
            print(connections)
            for client_id, connection in connections.items():
                print(f"Notifying client {client_id} with connection {connection}")
                try:
                    await connection.send_json({
                        "client_id": client_id,
                        "model_id": model_id,
                        "model_name": model_name,
                        "message": message,
                    })
                    print(f'Notified user: {client_id}')
                except Exception as e:
                    print(f'NotificationService Error: {e}')
