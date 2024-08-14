# app/routes/audio.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session

from fastapi.responses import StreamingResponse
import os
from app.services.social_media.conversation.audio_handler import process_audio_and_return_combined_results, generate_id, get_audio_uri
from app.repositories.social_media.conversation.categories.sub_categories.sub_category_repo import SubCategoryRepo
from app.database.connection import get_db
from fastapi import APIRouter, Request, HTTPException
from google.cloud import storage
from starlette.responses import StreamingResponse
# Load environment variables
GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
GCS_PROJECT_FOLDER = os.getenv('GCS_PROJECT_FOLDER')

router = APIRouter()

# Instantiating respective model repository classes
subCategoryRepo = SubCategoryRepo()


@router.post("/post-audio")
async def post_audio(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    sub_cat_id: str = None,
    mode: str = Query(..., regex="^(training|interview)$"),
    db: Session = Depends(get_db),
):
    # Retrieve category ID from the repository
    cat_id = subCategoryRepo.get(db, sub_cat_id, request).category_id

    # Generate a unique ID and audio URI
    audio_folder = f"storage/audio/cat-{cat_id}"
    os.makedirs(audio_folder, exist_ok=True)

    file_extension = '.webm'
    my_id = generate_id()
    my_info = {'id': my_id, 'audio_uri': get_audio_uri(
        cat_id, my_id, file_extension)}
    filename = os.path.join(audio_folder, f"{my_id}{file_extension}")

    with open(filename, 'wb') as f:
        f.write(file.file.read())
        file_path = f.name

    # Process the audio file and obtain results
    results = await process_audio_and_return_combined_results(
        db,
        request,
        audio_folder,
        file_path,
        sub_cat_id,
        my_info,
        mode,
        background_tasks,
    )

    return results


@router.get("/download-audio/{cat_name}/{filename}")
async def download_audio(request: Request, cat_name: str, filename: str, driver: str = 'gcs'):
    if driver.lower() == "local":
        audio_folder = f"storage/audio/{cat_name}"
        file_path = os.path.join(audio_folder, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        def iterfile():
            with open(file_path, mode="rb") as file_like:
                yield from file_like

        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    else:
        # Serve the file from GCS

        storage_client = storage.Client()

        # Define the GCS bucket and file path
        bucket_name = GOOGLE_CLOUD_STORAGE_BUCKET
        blob_path = f"{GCS_PROJECT_FOLDER}/audio/{cat_name}/{filename}"

        # Get the bucket and blob
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        # Check if the file exists in GCS
        if not blob.exists():
            # Log the details for debugging
            error_message = f"File not found: gs://{bucket_name}/{blob_path}"
            print(error_message)  # Log to console or a logging system
            raise HTTPException(status_code=404, detail=error_message)

        # Stream the file from GCS
        def iter_blob():
            with blob.open("rb") as file_like:
                yield from file_like

        return StreamingResponse(iter_blob(), media_type="audio/mpeg")
