import uuid
from uuid import UUID

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.user import crud_user
from src.models.user import User
from src.schemas.user import UserCreate, UserCreateDB, UserUpdate
from src.services.auth import hash_password


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


async def update_user(
    db: AsyncSession, update_schema: UserUpdate, user: User
) -> User:
    try:
        update_data = update_schema.model_dump(exclude_unset=True)

        updated_user = await crud_user.update(
            db=db,
            db_obj=user,
            update_data=update_data,
            commit=False,
        )
        await db.commit()
        await db.refresh(updated_user)
        return updated_user
    except Exception:
        await db.rollback()
        raise


async def make_superuser(
        db: AsyncSession,
        user_uid: UUID,
        is_superuser: bool,
        current_user: User
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can perform this action"
        )

    user = await crud_user.make_superuser(
        db=db,
        uid=user_uid,
        is_superuser=is_superuser
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


async def delete_user(
        db: AsyncSession,
        user_uid: UUID,
        current_user: User
) -> dict:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can perform this action"
        )

    if current_user.uid == user_uid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )

    success = await crud_user.delete_user(db, uid=user_uid)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"status": "success", "message": "User deleted"}