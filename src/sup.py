import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import User
from src.services.auth import hash_password


DATABASE_URL = "postgresql+asyncpg://admin:password@localhost:5432/audio_file_project"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_superuser():
    async for session in get_db():
        # Проверяем, не существует ли уже суперпользователя
        existing = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )
        if existing.scalar():
            print("Superuser already exists!")
            return

        # Создаем нового суперпользователя
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=await hash_password("51235678"),
            is_superuser=True
        )

        session.add(user)
        await session.commit()
        print(f"Superuser created successfully! ID: {user.id}")


if __name__ == "__main__":
    asyncio.run(create_superuser())