"""
Зависимости FastAPI для проверки авторизации по JWT (cookie).
- get_current_user: требует валидного access_token, возвращает пользователя или выбрасывает исключение
- get_optional_user: не выбрасывает, если токена нет (для опциональных сценариев)
- get_token: возвращает access_token из cookie (или выбрасывает исключение)

Кастомные исключения определены в app.exceptions.
"""

from datetime import UTC, datetime
from typing import Optional

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UsersDAO
from app.users.models import Users

def get_token(request: Request) -> str:
    """
    Извлекает JWT access_token из cookie "booking_access_token".
    Используется как зависимость для get_current_user.
    :raises TokenAbsentException: если cookie не найден
    :return: строка access_token
    """
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)) -> Users:
    """
    Декодирует JWT, валидирует срок действия, ищет пользователя по id.
    :param token: JWT access_token (из cookie)
    :raises IncorrectTokenFormatException: некорректный токен
    :raises TokenExpiredException: срок действия истёк
    :raises UserIsNotPresentException: пользователь не найден
    :return: ORM-модель пользователя (Users)
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise IncorrectTokenFormatException
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user

async def get_optional_user(request: Request) -> Optional[Users]:
    """
    Пытается извлечь и провалидировать JWT из cookie (если есть).
    Не выбрасывает ошибку, если токена или пользователя нет.
    :param request: FastAPI Request
    :return: ORM-модель пользователя (Users) или None
    """
    token = request.cookies.get("booking_access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return await UsersDAO.find_by_id(int(user_id))
    except JWTError:
        return None
