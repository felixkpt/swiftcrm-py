import os
from fastapi import HTTPException

# Custom imports
from app.services.openai_requests import convert_audio_to_text, get_chat_response
from app.models.conversation import store_messages
from app.services.text_to_speech import convert_text_to_speech
import uuid
from app.models.subcategory import get_cat_id


def generate_id():
    return str(uuid.uuid4())


def process_audio_and_return_combined_results(audio_input, sub_cat_id, my_info):

    # Ensure stored_audio folder exists
    cat_id = get_cat_id(sub_cat_id)
    audio_folder = f"storage/audio/cat-{cat_id}"

    os.makedirs(audio_folder, exist_ok=True)

    # Decode audio
    request_message = convert_audio_to_text(audio_file=audio_input)
    audio_input.close()

    # Guard: Ensure message decoded
    if not request_message:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get ChatGPT Response
    response_message = get_chat_response(
        message_content=request_message, sub_cat_id=sub_cat_id)

    assistant_id = generate_id()
    # Get the file extension from the dowloaded file
    file_extension = '.mp3'

    assistant_info = {'id': assistant_id,
                      'audio_uri': get_audio_uri(cat_id, assistant_id, file_extension)}

    my_info['message'] = request_message
    assistant_info['message'] = response_message

    # Save messages
    results = []
    if response_message:
        results = store_messages(sub_cat_id, my_info, assistant_info)
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

    return results


def get_audio_uri(cat_id, id, file_extension):
    return f"/download-audio/cat-{cat_id}/{id}{file_extension}"
