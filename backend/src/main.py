from fastapi import FastAPI
from src.database import Base, engine
from src.users.routers import referrals, users
from starlette.responses import HTMLResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение маршрутов
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(referrals.router, prefix="/api/v1/referrals", tags=["referrals"])


@app.get(
    "/",
    response_class=HTMLResponse,
)
def home():
    return f"""
    <html>
    <head><title>Referral system</title></head>
    <body>
    <ul>
    <li><a href="/docs">Документация Swagger</a></li>
    <li><a href="/redoc">Документация ReDoc</a></li>
    </ul>
    </body>
    </html>
    """