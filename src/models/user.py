from typing import List, Optional
import uuid
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    yandex_id: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())

    audio_files: Mapped[List["AudioFile"]] = relationship(
        "AudioFile",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )