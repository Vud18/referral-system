from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    referrer_code: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ReferralCreate(BaseModel):
    code: str
    expiry_date: datetime


class ReferralOut(BaseModel):
    id: str
    code: str
    expiry_date: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str | None = None


class ReferralCode(BaseModel):
    id: str
    code: str
    expiry_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: str
    username: str
    email: str
    referrer_code: str

    class Config:
        from_attributes = True
