"""
Модуль аутентификации пользователей:
- Хеширование и проверка паролей (bcrypt + passlib)
- Генерация JWT-токенов (с exp, alg из настроек)
- Аутентификация пользователя по email и паролю

ВНИМАНИЕ: Для корректной работы bcrypt требуется установить пакет pip install "passlib[bcrypt]"
"""

from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO

# Настройка passlib с использованием bcrypt для безопасного хранения паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Возвращает bcrypt-хеш пароля.
    :param password: Пароль в открытом виде
    :return: Хешированный пароль (str)
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли исходный пароль с хешем.
    :param plain_password: Обычный пароль пользователя
    :param hashed_password: Сохранённый хеш из БД
    :return: True если совпадает, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Генерирует JWT-токен для авторизации пользователя.
    :param data: Payload, например {"sub": user_id}
    :return: JWT-токен (строка)
    
    Время жизни токена берется из настроек settings.ACCESS_TOKEN_EXPIRE_MINUTES
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    """
    Проверяет существование пользователя и корректность пароля.
    :param email: email пользователя
    :param password: пароль пользователя
    :return: Объект пользователя или None (если не найден/неверный пароль)
    """
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
