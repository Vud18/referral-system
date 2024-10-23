import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.users import schemas
from src.users.models import ReferralCode, UserModel


async def get_user_by_email(db: Session, email: str):
    return await db.query(UserModel).filter(UserModel.email == email).first()


async def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """Функция создает пользователя в базе данных.
    Если не указан реферер код, то создает без него."""

    db_user = await UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    if user.referrer_code != "string":
        db_user = await UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            referrer_code=user.referrer_code,
        )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def create_referral_code(db: Session, user_id: int, expiry_days: int):
    """Функция создает реферальный код"""

    existing_code = (
        await db.query(ReferralCode)
        .filter(
            ReferralCode.user_id == user_id,
            ReferralCode.is_active == True,
            ReferralCode.expiry_date > datetime.utcnow(),
        )
        .first()
    )

    if existing_code:
        raise HTTPException(
            status_code=400, detail="Active referral code already exists"
        )

    expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

    new_code = await ReferralCode(
        code=str(uuid.uuid4()),
        expiry_date=expiry_date,
        user_id=user_id,
        is_active=True,
    )

    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    return new_code


async def delete_referral_code(
    db: Session,
    user_id: int,
):
    """Функция удаляет реферальный код, если такой имеется."""

    referral_code = (
        await db.query(ReferralCode)
        .filter(ReferralCode.user_id == user_id, ReferralCode.is_active == True)
        .first()
    )

    if not referral_code:
        raise HTTPException(status_code=404, detail="No active referral code found")

    # Деактивировать код
    referral_code.is_active = False
    db.commit()
    return referral_code


async def get_referrals_by_referrer_id(db: Session, referrer_id: str):
    """Возвращает всех пользователей которые зарегистрировались по referrer_code"""

    return db.query(UserModel).filter(UserModel.referrer_code == referrer_id).all()
