"""
Конфигурация приложения FastAPI.

- Загружает параметры из переменных окружения (.env).
- Описывает настройки для различных сред (DEV, TEST, PROD), баз данных, Redis, SMTP, секретов и логирования.
- Использует Pydantic BaseSettings.
"""

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Глобальные настройки приложения.

    Атрибуты:
        MODE: Режим запуска приложения ("DEV", "TEST", "PROD").
        LOG_LEVEL: Уровень логирования.
        HAWK_TOKEN: Токен Hawk для интеграций.
        
        --- Основная база данных ---
        DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME: параметры подключения к основной БД.
        DATABASE_URL: строка подключения к основной БД (генерируется автоматически).
        
        --- Тестовая база данных ---
        TEST_DB_HOST, TEST_DB_PORT, TEST_DB_USER, TEST_DB_PASS, TEST_DB_NAME: параметры тестовой БД.
        TEST_DATABASE_URL: строка подключения к тестовой БД.
        
        --- Секреты для JWT ---
        SECRET_KEY: секрет для JWT.
        ALGORITHM: алгоритм шифрования JWT.
        
        --- Redis ---
        REDIS_HOST, REDIS_PORT: параметры подключения к Redis.
        
        --- SMTP ---
        SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS: параметры почтового сервера.
    """

    # Общие параметры среды
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    HAWK_TOKEN: str  # Токен Hawk для внешних интеграций

    # Основная база данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """URL подключения к основной базе данных (PostgreSQL/asyncpg)."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Тестовая база данных (используется для автотестов/CI)
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self) -> str:
        """URL подключения к тестовой базе данных."""
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    # Секреты для JWT
    SECRET_KEY: str
    ALGORITHM: str

    # Redis (кеш)
    REDIS_HOST: str
    REDIS_PORT: int

    # SMTP (почтовый сервер для уведомлений и подтверждений)
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    # Конфиг Pydantic: путь к .env файлу (все переменные среды читаются оттуда)
    model_config = SettingsConfigDict(env_file=".env")  # .env лежит в корне проекта

settings = Settings()
