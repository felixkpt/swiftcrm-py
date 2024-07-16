# app/routes/audio.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
import os
from app.services.audio_handler import process_audio_and_return_combined_results, generate_id, get_audio_uri
from app.repositories.conversation.v1.sub_category import SubCategoryRepo

router = APIRouter()


@router.post("/post-audio")
async def post_audio(file: UploadFile = File(...), sub_cat_id: str = None, mode: str = Query(..., regex="^(training|interview)$")):
    cat_id = SubCategoryRepo.get_cat_id(sub_cat_id)
    audio_folder = f"storage/audio/cat-{cat_id}"
    os.makedirs(audio_folder, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1]
    my_id = generate_id()
    my_info = {'id': my_id, 'audio_uri': get_audio_uri(
        cat_id, my_id, file_extension)}
    filename = os.path.join(audio_folder, f"{my_id}{file_extension}")

    with open(filename, 'wb') as f:
        f.write(file.file.read())

    results = []
    with open(filename, 'rb') as audio_input:
        results = process_audio_and_return_combined_results(
            audio_input, sub_cat_id, my_info, mode)

    return results


@router.get("/download-audio/{cat_name}/{filename}")
async def download_audio(cat_name: str, filename: str):
    audio_folder = f"storage/audio/{cat_name}"
    file_path = os.path.join(audio_folder, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(file_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
