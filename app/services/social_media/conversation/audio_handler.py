import os
import uuid
from fastapi import HTTPException, BackgroundTasks, Depends, Request

# Custom imports
from app.services.social_media.conversation.openai_requests import convert_audio_to_text, get_chat_message_response
from app.repositories.social_media.conversation.conversation_repo import ConversationRepo
from app.services.social_media.conversation.google_requests import convert_text_to_speech, upload_to_gcs, transcribe_speech
from app.repositories.social_media.conversation.categories.sub_categories.sub_category_repo import SubCategoryRepo

# Instantiate model repository classes
subCategoryRepo = SubCategoryRepo()
conversationRepo = ConversationRepo()

def generate_id():
    return str(uuid.uuid4())

async def process_audio_and_return_combined_results(db, request, audio_folder, source_file_name, sub_cat_id, my_info, mode='training', background_tasks: BackgroundTasks = None):

    # Get the file extension from the downloaded file
    file_extension = '.webm'
    cat_id = subCategoryRepo.get(db, sub_cat_id).category_id
    id = my_info['id']

    destination_file_name = f'audio/cat-{cat_id}/{id}{file_extension}'

    # Upload user audio file to Google Cloud Storage (running in the background)
    background_tasks.add_task(upload_to_gcs, source_file_name, destination_file_name)
    
    # Convert user speech to text (Google Speech-to-Text transcription)
    google_transcript = transcribe_speech(source_file_name)
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
        response = await conversationRepo.store_messages(
            db, request, sub_cat_id, my_info, assistant_info, mode, interview_id)
        records = response['records']
        if records:
            my_info = records[0]
            assistant_info = records[1]

    # Convert text to speech
    destination_file_name = f'audio/cat-{cat_id}/{assistant_id}{file_extension}'
    file_path = convert_text_to_speech(
        response_message, 'storage/'+destination_file_name)

    # Guard: Ensure message decoded to audio
    if not response:
        raise HTTPException(
            status_code=400, detail="Failed to get Google Text-to-Speech response")

    # Upload assistant audio file to Google Cloud Storage in the background
    background_tasks.add_task(upload_to_gcs, file_path, destination_file_name)

    return response

def get_audio_uri(cat_id, id, file_extension):
    return f"/social-media/conversation/download-audio/cat-{cat_id}/{id}{file_extension}"
