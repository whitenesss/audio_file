from sqlalchemy.ext.asyncio import AsyncSession
from src.models import AudioFile

class CRUDAudio:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_audio_file(
        self,
        user_id: int,
        file_name: str,
        file_path: str
    ) -> AudioFile:
        audio_file = AudioFile(
            user_id=user_id,
            file_name=file_name,
            file_path=file_path
        )
        self.session.add(audio_file)
        await self.session.commit()
        await self.session.refresh(audio_file)
        return audio_file

    async def get_user_audio_files(
        self,
        user_id: int
    ) -> list[AudioFile]:
        from sqlalchemy import select
        stmt = select(AudioFile).where(AudioFile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()