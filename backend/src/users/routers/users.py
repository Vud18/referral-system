from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src import crud
from src.database import get_db
from src.users import schemas
from src.users.services import auth

router = APIRouter()


@router.post(
    "/register",
    response_model=schemas.Token,
    summary="Регистрация нового пользователя.",
)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя."""

    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)
    user = crud.create_user(db, user, hashed_password)
    access_token = auth.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Получить токен.",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Возвращает токен пользователя."""

    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
