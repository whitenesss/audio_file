from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_db
from src.models import User
from src.schemas.user import UserResponse, UserSuperuserUpdate
from src.services import user_service
from src.services.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.patch("/make_superuser/", response_model=UserResponse)
async def make_superuser(
    update_data: UserSuperuserUpdate,
    user_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.make_superuser(
        db=db,
        user_uid=user_uid,
        is_superuser=update_data.is_superuser,
        current_user=current_user
    )

@router.delete("/delete_user/")
async def admin_delete_user(
    user_uid: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.delete_user(
        db=db,
        user_uid=user_uid,
        current_user=current_user
    )