import uuid

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import crud_user
from src.models.user import User
from src.schemas.user import UserCreate, UserCreateDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(
        db: AsyncSession,
        create_data: UserCreate,
) -> User:

    try:
        create_data_dict = create_data.model_dump(exclude_unset=True)
        hashed_password = await hash_password(create_data_dict.pop("password"))
        random_uid = str(uuid.uuid4())

        user_created = await crud_user.create(
            db=db,
            create_schema=UserCreateDB(
                            uid=random_uid,
                            hashed_password=hashed_password,
                            **create_data_dict,
                            commit=False,
                        ),
        )
        await db.flush()
        await db.commit()
    except Exception:
       await db.rollback()
       raise
    return user_created


