from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AudioFile(Base):
    __tablename__ = "audio_file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="audio_files",
        lazy="selectin"
    )