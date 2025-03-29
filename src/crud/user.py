from typing import Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, load_only

from src.models.user import User
from src.schemas.user import UserUpdateDB

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class CRUDUser:
    def __init__(self, model: Type[ModelType]):
        self.model = model
    async def create(
        self,
        db: AsyncSession,
        *,
        create_schema: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj

    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_uid_fast(
        self, db: AsyncSession, *, uid: UUID
    ) -> Optional[User]:
        statement = (
            select(self.model)
            .where(
                self.model.uid == uid
            )
            .options(
                load_only(
                    self.model.id,
                    self.model.uid,

                )
            )
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def make_superuser(
            self,
            db: AsyncSession,
            *,
            uid: UUID,
            is_superuser: bool,
            commit: bool = True
    ) -> Optional[User]:
        stmt = (
            update(self.model)
            .where(self.model.uid == uid)
            .values(is_superuser=is_superuser)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        user = result.scalars().first()
        if commit:
            await db.commit()
            if user:
                await db.refresh(user)
        return user

    async def delete_user(
            self,
            db: AsyncSession,
            *,
            uid: UUID,
            commit: bool = True
    ) -> bool:
        stmt = delete(self.model).where(self.model.uid == uid)
        result = await db.execute(stmt)
        if commit:
            await db.commit()
        return result.rowcount > 0

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        update_data: Union[UserUpdateDB, dict],
        commit: bool = True,
    ) -> User:

        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)

        stmt = (
            update(self.model)
            .where(self.model.id == db_obj.id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if commit:
            await db.commit()
            await db.refresh(obj)
        return obj
    async def get_user_with_full_options(
        self, db: AsyncSession, *, user_id: int
    ) -> Optional[User]:

        statement = (
            select(self.model)
            .where(self.model.id == user_id)
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def delete(self, db: AsyncSession, *, db_obj: User, commit: bool = True):
        stmt = delete(self.model).where(self.model.id == db_obj.id)
        await db.execute(stmt)
        if commit:
            await db.commit()

    async def get_by_service_id(
        self,
        db: AsyncSession,
        *,
        service_id_field: str,
        user_service_id: str,
    ) -> Optional[User]:
        statement = select(self.model).where(
            getattr(self.model, service_id_field) == user_service_id
        )
        result = await db.execute(statement)
        return result.scalars().first()
    async def get_users_all(self, db: AsyncSession):
        statement = select(self.model)
        result = await db.execute(statement)
        return result.scalars().all()


crud_user = CRUDUser(User)

async def get_by_uid(db: AsyncSession, *, uid: UUID) -> Optional[User]:
    statement = (
        select(User)
        .where(
            User.uid == uid,
        )
    )
    result = await db.execute(statement)
    return result.scalars().first()