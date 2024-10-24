import pytest
import pytest_asyncio
from starlette import status

from src.users.routers.users import auth_router
from src.users.schemas import UserCreate
from tests.conftest import faker
from tests.integration.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestAuthRouter(BaseTestRouter):
    # Указываем роутер, который будем тестировать:
    router = auth_router

    @pytest_asyncio.fixture
    async def user(self) -> UserCreate:
        """Данные пользователя для тестов регистрации и логина."""
        return UserCreate(
            username="string", email="string", password="string", referrer_code="string"
        )

    # MARK: POST
    async def test_register_post_route(self, router_client, user):
        """Регистрация пользователя с корректными данными."""
        response = await router_client.post(
            "/register",
            json={
                "username": faker.user_name(),
                "email": faker.email(),
                "password": faker.password(),
                "referrer_code": "string",
            },
        )
        assert response.status_code == 201

    async def test_login_post_route(self, router_client, user: UserCreate):
        """Зарегистрированный пользователь может залогиниться."""

        response = await router_client.post(
            "/register",
            json={
                "username": "string",
                "email": "string",
                "password": "string",
                "referrer_code": "string",
            },
        )

        assert response.status_code == 201

        response = await router_client.post(
            "/login",
            json={"username": user.username, "password": user.password},
        )

        token = response.json()

        assert response.status_code == 200

        assert token["access_token"] is not None
        assert token["token_type"] == "bearer"
        assert response.status_code == status.HTTP_200_OK
