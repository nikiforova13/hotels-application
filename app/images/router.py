import aiofiles
from fastapi import APIRouter, UploadFile

from app.tasks_celery.tasks import process_picture

router = APIRouter(prefix="/images", tags=["Download images"])


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    path = f"app/static/images/{name}.webp"
    async with aiofiles.open(path, "wb+") as file_object:
        file = await file.read()
        await file_object.write(file)
    process_picture.delay(path)
    # webp - сжимать картинки без потери качества
