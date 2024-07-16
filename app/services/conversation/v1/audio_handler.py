# app/services/audio_handler.py
import os
from fastapi import HTTPException

# Custom imports
from app.services.conversation.v1.openai_requests import convert_audio_to_text, get_chat_response
from app.repositories.conversation.v1.conversation_repo import ConversationRepo

from app.services.conversation.v1.text_to_speech import convert_text_to_speech
import uuid
from app.repositories.conversation.v1.sub_category import SubCategoryRepo


def generate_id():
    return str(uuid.uuid4())


def process_audio_and_return_combined_results(audio_input, sub_cat_id, my_info, mode='training'):
    # Ensure stored_audio folder exists
    cat_id = SubCategoryRepo.get_cat_id(sub_cat_id)
    audio_folder = f"storage/audio/cat-{cat_id}"

    os.makedirs(audio_folder, exist_ok=True)

    # Decode audio
    request_message = convert_audio_to_text(audio_file=audio_input)
    audio_input.close()

    # Guard: Ensure message decoded
    if not request_message:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get ChatGPT Response
    messages, interview_id = ConversationRepo.get_recent_messages(sub_cat_id, mode)
    
    response_message, interview_id = get_chat_response(
        messages, interview_id, message_content=request_message, sub_cat_id=sub_cat_id, mode=mode)

    assistant_id = generate_id()
    # Get the file extension from the downloaded file
    file_extension = '.mp3'

    assistant_info = {'id': assistant_id,
                      'audio_uri': get_audio_uri(cat_id, assistant_id, file_extension)}

    my_info['message'] = request_message
    assistant_info['message'] = response_message

    # Save messages
    response = []
    if response_message:
        response = ConversationRepo.store_messages(
            sub_cat_id, my_info, assistant_info, mode, interview_id)
        results = response['results']
        if results:
            my_info = results[0]
            assistant_info = results[1]
    else:
        print('No response message')

    # Convert text to speech
    response_audio_filename = convert_text_to_speech(
        response_message, os.path.join(audio_folder, f"{assistant_id}.mp3"))

    # Guard: Ensure message decoded to audio
    if not response_audio_filename:
        raise HTTPException(
            status_code=400, detail="Failed to get Google Text-to-Speech response")

    return response


def get_audio_uri(cat_id, id, file_extension):
    return f"/conversation/v1/download-audio/cat-{cat_id}/{id}{file_extension}"
