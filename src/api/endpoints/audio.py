from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_db
from src.models import User
from src.schemas.audio import AudioFileCreate, AudioFileResponse
from src.services.auth import get_current_user
from src.services.audio import AudioService

router = APIRouter(prefix="/audio", tags=["audio"])

@router.post("/upload/", response_model=AudioFileCreate)
async def upload_audio(
    file_name: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    service = AudioService(db)
    return await service.upload_audio(current_user, file_name, file)

@router.get("/my-files/", response_model=list[AudioFileResponse])
async def get_my_files(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    service = AudioService(db)
    return await service.get_user_files(user)






# import os
#
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database import get_async_db
# from src.models import User, AudioFile
# from src.schemas.audio import AudioFileCreate, AudioFileResponse
# from src.services.auth import get_current_user
#
# router = APIRouter(prefix="/audio", tags=["audio"])
#
# UPLOAD_DIR = "src/static/"
#
# ALLOWED_AUDIO_TYPES = [
#     'audio/mpeg',
#     'audio/wav',
#     'audio/x-wav',
#     'audio/aac',
#     'audio/ogg',
#     'audio/x-m4a',
# ]
#
#
# def validate_audio_file(file: UploadFile):
#     audio_signatures = {
#         b'ID3': 'audio/mpeg',  # MP3
#         b'RIFF': 'audio/wav',  # WAV
#         b'OggS': 'audio/ogg',  # OGG
#     }
#
#     # Читаем первые несколько байт файла
#     header = file.file.read(4)
#     file.file.seek(0)
#
#     for signature, mime in audio_signatures.items():
#         if header.startswith(signature):
#             if file.content_type != mime:
#                 raise ValueError(f"Файл имеет сигнатуру {mime}, но Content-Type: {file.content_type}")
#             return
#
#     raise ValueError("Файл не является валидным аудио")
#
# @router.post("/upload/", response_model=AudioFileCreate )
# async def upload_audio(
#         file_name: str,
#         file: UploadFile = File(...),
#         current_user: User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_async_db),
# ):
#     if file.content_type not in ALLOWED_AUDIO_TYPES:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Недопустимый тип файла. Разрешены: {', '.join(ALLOWED_AUDIO_TYPES)}"
#         )
#     try:
#         validate_audio_file(file)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#     allowed_extensions = ['.mp3', '.wav', '.aac', '.ogg', '.m4a']
#     file_ext = os.path.splitext(file.filename)[1].lower()
#     if file_ext not in allowed_extensions:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Недопустимое расширение файла. Разрешены: {', '.join(allowed_extensions)}"
#         )
#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file_name}")
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())
#
#     audio_file = AudioFile(
#         user_id=current_user.id,
#         file_name=file_name,
#         file_path=file_path
#     )
#     db.add(audio_file)
#     await db.commit()
#     await db.refresh(audio_file)
#
#     return {
#         "message": "File uploaded successfully",
#         "file_id": audio_file.id,
#         "file_name": audio_file.file_name,
#         "file_path": audio_file.file_path
#     }
#
#
# @router.get("/my-files/", response_model=list[AudioFileResponse])
# async def get_my_files(
#     user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_async_db),
# ):
#     files = user.audio_files
#     return files