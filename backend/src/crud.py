import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import schemas
from src.users.models import ReferralCode, UserModel


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate, hashed_password: str):
    """Функция создает пользователя в базе данных.
    Если не указан реферер код, то создает без него."""

    db_user = UserModel(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        referrer_code=user.referrer_code if user.referrer_code != "string" else None,
    )

    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        await db.rollback()  # Откатываем транзакцию в случае ошибки
        print(f"Error while creating user: {e}")
        raise e

    return db_user


async def create_referral_code(db: AsyncSession, user_id: int, expiry_days: int):
    """Функция создает реферальный код"""

    existing_code = await db.execute(
        select(ReferralCode).where(
            ReferralCode.user_id == user_id,
            ReferralCode.is_active == True,
            ReferralCode.expiry_date > datetime.utcnow(),
        )
    )
    existing_code = existing_code.scalars().first()

    if existing_code:
        raise HTTPException(
            status_code=400, detail="Active referral code already exists"
        )

    expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

    new_code = ReferralCode(
        code=str(uuid.uuid4()),
        expiry_date=expiry_date,
        user_id=user_id,
        is_active=True,
    )

    db.add(new_code)
    await db.commit()
    await db.refresh(new_code)

    return new_code


async def delete_referral_code(
    db: AsyncSession,
    user_id: int,
):
    """Функция удаляет реферальный код, если такой имеется."""

    result = await db.execute(
        select(ReferralCode).where(
            ReferralCode.user_id == user_id, ReferralCode.is_active == True
        )
    )
    referral_code = result.scalars().first()

    if not referral_code:
        raise HTTPException(status_code=404, detail="No active referral code found")

    # Деактивировать код
    referral_code.is_active = False
    await db.commit()

    return referral_code


async def get_referrals_by_referrer_id(db: AsyncSession, referrer_id: str):
    """Возвращает всех пользователей которые зарегистрировались по referrer_code"""

    # Подзапрос для получения реферального кода реферера
    referral_code_subquery = (
        select(ReferralCode.code)
        .where(ReferralCode.user_id == referrer_id)
        .scalar_subquery()
    )

    # Основной запрос для получения пользователей, которые указали данный реферальный код
    result = await db.execute(
        select(UserModel).where(UserModel.referrer_code == referral_code_subquery)
    )

    referrals = result.scalars().all()

    return referrals
