from fastapi import UploadFile, APIRouter
import aiofiles
router = APIRouter(prefix='/images', tags=['Download images'])

@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    async with aiofiles.open(f"app/static/images/{name}.webp", "wb+") as file_object:
        file = await file.read()
        await file_object.write(file)
        # webp - сжимать картинки без потери качества

