# app/services/audio_handler.py
import os
from fastapi import HTTPException

# Custom imports
from app.services.social_media.conversation.openai_requests import convert_audio_to_text, get_chat_message_response
from app.repositories.social_media.conversation.conversation_repo import ConversationRepo
from fastapi import Request, Depends
from app.services.social_media.conversation.google_requests import convert_text_to_speech, upload_to_gcs, transcribe_speech
import uuid
from app.repositories.social_media.conversation.categories.sub_categories.sub_category_repo import SubCategoryRepo


# Instantiate model repository classes
subCategoryRepo = SubCategoryRepo()
conversationRepo = ConversationRepo()


def generate_id():
    return str(uuid.uuid4())


async def process_audio_and_return_combined_results(db, request, source_file_name, sub_cat_id, my_info, mode='training'):

    # Get the file extension from the downloaded file
    file_extension = '.webm'
    # Ensure stored_audio folder exists
    cat_id = subCategoryRepo.get(db, sub_cat_id).category_id
    local_audio_folder = f"storage/audio/cat-{cat_id}"
    os.makedirs(local_audio_folder, exist_ok=True)

    id = my_info['id']

    destination_file_name = f'audio/cat-{cat_id}/{id}{file_extension}'

    # Upload user audio file to Google Cloud Storage
    gcs_uri = upload_to_gcs(source_file_name, destination_file_name)

    # Convert user speeach to text (Google Speech-to-Text transcription)
    google_transcript = transcribe_speech(gcs_uri)
    print("Google Transcription:", google_transcript)
    request_message = google_transcript['transcript_text']
    word_confidences = google_transcript['word_confidences']

    # Guard: Ensure message decoded
    if not request_message:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get ChatGPT Response
    messages, interview_id = await conversationRepo.get_recent_messages(
        db, request, sub_cat_id, mode)

    response_message, interview_id = get_chat_message_response(
        messages, interview_id, message_content=request_message, sub_cat_id=sub_cat_id, mode=mode)

    assistant_id = generate_id()

    assistant_info = {'id': assistant_id,
                      'audio_uri': get_audio_uri(cat_id, assistant_id, file_extension)}

    my_info['message'] = request_message
    my_info['word_confidences'] = word_confidences
    assistant_info['message'] = response_message

    # Save messages
    response = []
    if response_message:
        response = conversationRepo.store_messages(
            db, request, sub_cat_id, my_info, assistant_info, mode, interview_id)
        records = response['records']
        if records:
            my_info = records[0]
            assistant_info = records[1]
    else:
        print('No response message')

    # Convert text to speech
    destination_file_name = f'audio/cat-{cat_id}/{assistant_id}{file_extension}'
    response_audio_filename = convert_text_to_speech(
        response_message, destination_file_name)

    # Guard: Ensure message decoded to audio
    if not response_audio_filename:
        raise HTTPException(
            status_code=400, detail="Failed to get Google Text-to-Speech response")

    return response


def get_audio_uri(cat_id, id, file_extension):
    return f"/social-media/conversation/download-audio/cat-{cat_id}/{id}{file_extension}"
