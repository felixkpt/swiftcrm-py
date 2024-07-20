# events/notifications.py
from app.websocket.websocket_manager import WebSocketManager

class NotificationService:
    def __init__(self, websocket_manager: WebSocketManager):
        self.websocket_manager = websocket_manager

    async def notify_model_updated(self, model_id: str, message: str):
        """Notify all clients about a model update."""
        await self.websocket_manager.broadcast(message)

    async def notify_new_interview_results(self, interview_id: str):
        """Notify a specific client about new interview results."""
        message = f"New results available for interview {interview_id}"
        await self.websocket_manager.send_personal_message(message)
