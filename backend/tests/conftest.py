import asyncio

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base

from faker import Faker

faker = Faker()

engine_test = create_async_engine(
    url="sqlite+aiosqlite:///./pytest.db",
    echo=True,
)

async_session_maker = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(
    autouse=True,
    scope="module",
)
async def prepare_database():
    """Сбрасываем и создаем таблицы в БД перед запуском каждого модуля с тестами, и снова сбрасываем
    после прогона каждого модуля."""

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session():
    """
    Параметр `scope="function"` обеспечивает запуск этой фикстуры перед запуском каждого
    теста. Так что после запуска каждого теста, данные в БД откатываются. Каждый тест работает
    изолированно от других.
    """
    async with engine_test.connect() as conn:
        tsx = await conn.begin()
        async with async_session_maker(bind=conn) as _session:
            nested_tsx = await conn.begin_nested()

            yield _session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    """
    Фикстура event_loop ограничена всей сессией тестирования и позволяет Pytest
    иметь только один активный цикл событий на весь тестовый запуск. Встроенная
    фикстура цикла событий с pytest-asyncio по умолчанию ограничена функцией, и ее использование
    приведет к ошибке Pytest с большим количеством ошибок закрытия/открытия цикла.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
