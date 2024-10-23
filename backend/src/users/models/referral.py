import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=str(uuid.uuid4())
    )
    code: Mapped[str] = mapped_column(unique=True, index=True)
    expiry_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    user_id: Mapped[str] = mapped_column(String, sa.ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    owner = relationship("UserModel", back_populates="referral_code")
