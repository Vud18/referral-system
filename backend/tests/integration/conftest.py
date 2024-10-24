import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.database import get_db
from src.main import app as the_app


@pytest_asyncio.fixture(scope="function")
async def client(session):
    """Клиент для интеграционных тестов эндпоинтов."""

    the_app.dependency_overrides[get_db] = lambda: session
    async with AsyncClient(app=the_app, base_url="http://test") as async_client:
        yield async_client


class BaseTestRouter:
    """Класс для тестирования роутов."""

    @pytest_asyncio.fixture(scope="function")
    async def router_client(self, session):
        app = FastAPI()
        app.include_router(self.router)
        app.dependency_overrides[get_db] = lambda: session
        async with AsyncClient(app=app, base_url="http://test") as async_client:
            yield async_client
