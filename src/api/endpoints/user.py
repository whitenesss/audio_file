from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.user import crud_user
from src.database import get_async_db
from src.models import User
from src.schemas.user import UserResponse, UserCreate, UserUpdate
from src.services import user_service
from src.services.auth import get_current_user

router = APIRouter()

@router.get("",
            response_model=list[UserResponse],
            description="Get all users",)
async def get_users(
        db: AsyncSession = Depends(get_async_db),
):
    return await crud_user.get_users_all(db)


@router.post(
    "/",
    response_model=UserResponse,
    description="Create a new user",
)
async def create_user(
        request: Request,
        create_data: UserCreate,
        db: AsyncSession = Depends(get_async_db),

):
    user = await crud_user.get_by_email(db, email=create_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {create_data.email} is already "
                   "associated with an account.",
        )
    new_user = await user_service.create_user(
        db=db,
        create_data=create_data
    )
    return new_user

@router.patch("/update_user/", response_model=UserResponse
              )
async def update_user(
        update_data: UserUpdate,
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user),
):
    await user_service.update_user(
        db=db, update_schema=update_data, user=current_user
    )
    refreshed_user = await crud_user.get_user_with_full_options(
        db=db, user_id=current_user.id
    )
    return refreshed_user

