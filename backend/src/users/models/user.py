import uuid

from sqlalchemy import String
from sqlalchemy import String as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

__all__ = ["UserModel"]


class UserModel(Base):
    """Основная модель пользователей."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    referrer_code: Mapped[str] = mapped_column(nullable=True)
    referral_code = relationship("ReferralCode", back_populates="owner")
