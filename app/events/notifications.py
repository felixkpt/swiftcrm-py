# events/notifications.py
from app.websocket.websocket_manager import WebSocketManager


async def notify_model_updated(model_id: str, message: str):
    await WebSocketManager.broadcast(message)


async def notify_new_interview_results(interview_id: str):
    message = f"New results available for interview {interview_id}"
    await WebSocketManager.send_personal_message(message)
