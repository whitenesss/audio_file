from typing import Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.models.user import User

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



crud_user = CRUDUser(User)