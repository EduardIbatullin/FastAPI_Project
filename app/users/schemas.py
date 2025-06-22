"""
Pydantic-схемы и перечисления для пользователей.
- UserRoleEnum: роли пользователя для сериализации в API (ответы, OpenAPI)
- SUserAuth: схема для входа/регистрации (email + пароль)
- SUserOut: схема ответа с инфо о пользователе (id, email, роль)
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr

class UserRoleEnum(str, Enum):
    """
    Роли пользователя для сериализации в ответах API:
    - USER: обычный пользователь
    - DEVELOPER: разработчик (расширенные права)
    - ADMIN: администратор (максимальные права)
    """
    USER = "Пользователь"
    DEVELOPER = "Разработчик"
    ADMIN = "Администратор"

class SUserAuth(BaseModel):
    """
    Схема для аутентификации (логин и регистрация пользователя).
    Используется как входная схема (email и пароль).
    """
    email: EmailStr  # Валидация email по стандарту RFC
    password: str

class SUserOut(BaseModel):
    """
    Схема пользователя для выдачи через API (response_model).
    Используется для эндпоинта /auth/me.
    """
    id: int
    email: EmailStr
    role: UserRoleEnum

    # Позволяет напрямую возвращать ORM-модель как response_model FastAPI
    model_config = ConfigDict(from_attributes=True)
