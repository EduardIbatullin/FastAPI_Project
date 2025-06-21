"""
Модуль инициализации асинхронной работы с базой данных через SQLAlchemy.

- Автоматически выбирает конфигурацию для основной или тестовой БД.
- Для тестовой среды используется NullPool (без connection pool'а).
- Создаёт фабрику асинхронных сессий и базовый класс для моделей.
"""

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Определяем параметры подключения в зависимости от окружения.
# Для тестов: отдельный URL и отключённый pool (NullPool), чтобы каждый тест был изолирован.
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAM = {"poolclass": NullPool}  # NullPool = без пула, соединения создаются по запросу
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAM = {}

# Создаём асинхронный engine и фабрику сессий для работы с БД.
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAM)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
# async_session_maker используется для создания асинхронных сессий:
# async with async_session_maker() as session: ...

class Base(DeclarativeBase):
    """Базовый класс SQLAlchemy для всех моделей проекта."""
    pass
