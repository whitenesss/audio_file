import os
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.audio import CRUDAudio
from src.models import User


class AudioService:
    def __init__(self, session: AsyncSession):
        self.crud = CRUDAudio(session)
        self.upload_dir = Path("src/static")
        self.allowed_types = [
            'audio/mpeg', 'audio/wav', 'audio/x-wav',
            'audio/aac', 'audio/ogg', 'audio/x-m4a'
        ]
        self.allowed_extensions = ['.mp3', '.wav', '.aac', '.ogg', '.m4a']

    async def validate_audio_file(self, file: UploadFile):
        audio_signatures = {
            b'ID3': 'audio/mpeg',
            b'RIFF': 'audio/wav',
            b'OggS': 'audio/ogg',
        }
        header = file.file.read(4)
        file.file.seek(0)
        for signature, mime in audio_signatures.items():
            if header.startswith(signature):
                if file.content_type != mime:
                    raise ValueError(f"Файл имеет сигнатуру {mime}, но Content-Type: {file.content_type}")
                return
        raise ValueError("Файл не является валидным аудио")

    async def upload_audio(
            self,
            user: User,
            file_name: str,
            file: UploadFile
    ) -> dict:
        if file.content_type not in self.allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимый тип файла. Разрешены: {', '.join(self.allowed_types)}"
            )

        try:
            await self.validate_audio_file(file)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимое расширение файла. Разрешены: {', '.join(self.allowed_extensions)}"
            )

        self.upload_dir.mkdir(exist_ok=True)
        file_path = self.upload_dir / f"{user.id}_{file_name}"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        audio_file = await self.crud.create_audio_file(
            user_id=user.id,
            file_name=file_name,
            file_path=str(file_path)
        )
        return {
            "message": "File uploaded successfully",
            "file_id": audio_file.id,
            "file_name": audio_file.file_name,
            "file_path": audio_file.file_path
        }

    async def get_user_files(self, user: User) -> list:
        return await self.crud.get_user_audio_files(user.id)