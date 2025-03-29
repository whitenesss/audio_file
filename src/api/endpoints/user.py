from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.user import crud_user
from src.database import get_async_db
from src.schemas.user import UserResponse, UserCreate
from src.services import user_service

router = APIRouter()

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