"""
Pytest-фикстуры для тестирования FastAPI-приложения:
- Пересоздаёт тестовую БД, наполняет мок-данными из JSON
- Возвращает асинхронных клиентов (авторизованный и нет)
- Гарантирует: работает только если settings.MODE == "TEST"
"""

import asyncio
import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.main import app as fastapi_app
from app.users.models import Users

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Пересоздаёт тестовую БД и наполняет её мок-данными из mock_*.json.
    Запускается автоматически для всех тестов (scope='session').
    Безопасность: работает только при settings.MODE == "TEST"!
    """
    assert settings.MODE == "TEST", "Тестовые фикстуры могут работать только в тестовом режиме!"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        """Пробует открыть и прочитать mock_*.json, кидает исключение при ошибке."""
        try:
            with open(f"app/tests/mock_{model}.json", encoding="utf8") as file:
                return json.load(file)
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки mock_{model}.json: {e}")

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")
    # Преобразуем даты в datetime
    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        await session.execute(insert(Hotels).values(hotels))
        await session.execute(insert(Rooms).values(rooms))
        await session.execute(insert(Users).values(users))
        await session.execute(insert(Bookings).values(bookings))
        await session.commit()

@pytest.fixture(scope="function")
async def ac():
    """
    Асинхронный httpx-клиент для тестирования FastAPI (без авторизации).
    :yield: AsyncClient
    """
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_ac():
    """
    Асинхронный httpx-клиент с авторизацией.
    Делает login через /auth/login (email=test@test.com, password=test).
    Требует, чтобы такой пользователь был в mock_users.json!
    :yield: AsyncClient с валидной cookie 'booking_access_token'
    """
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        resp = await ac.post("/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        assert ac.cookies.get("booking_access_token"), "Не удалось получить access_token, проверьте тестовые данные."
        yield ac

@pytest.fixture(scope="function")
async def session():
    """
    Асинхронная сессия SQLAlchemy для прямых операций с БД (scope=function).
    :yield: AsyncSession
    """
    async with async_session_maker() as session:
        yield session

# Если потребуется event_loop для Windows/asyncio, раскомментируйте и настройте:
# @pytest.fixture(scope="session")
# def event_loop():
#     """
#     Для поддержки асинхронных тестов на Windows.
#     """
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
