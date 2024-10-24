from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.crud import get_referrals_by_referrer_id
from src.database import get_db
from src.users import schemas
from src.users.models import UserModel
from src.users.schemas import UserSchema
from src.users.services.auth import get_current_user

referral_router = APIRouter()


@referral_router.post(
    "/referral/create",
    response_model=schemas.ReferralCode,
    summary="Создать реферальный код.",
)
async def create_referral_code(
    expiry_days: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Создает реферальный код пользователю. Доступен авторизованному пользователю."""

    if expiry_days <= 0:
        raise HTTPException(
            status_code=400, detail="Expiry days must be greater than 0"
        )

    return await crud.create_referral_code(
        db, user_id=current_user.id, expiry_days=expiry_days
    )


@referral_router.delete(
    "/referral/delete",
    response_model=schemas.ReferralCode,
    summary="Удалить уже имеющийся реферальный код.",
)
async def delete_referral_code(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Функция удаляет реферальный код. Доступен авторизованному пользователю"""

    return await crud.delete_referral_code(db, user_id=current_user.id)


@referral_router.get(
    "/referrals/{referrer_code}",
    response_model=list[UserSchema],
    summary="Получение 	информации о рефералах по referrer_code.",
)
async def get_referrals(referrer_id: str, db: AsyncSession = Depends(get_db)):
    referrals = await get_referrals_by_referrer_id(db, referrer_id)

    if not referrals:
        raise HTTPException(
            status_code=404, detail="No referrals found for this referrer ID"
        )
    return referrals
