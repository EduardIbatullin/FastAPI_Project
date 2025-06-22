"""
SQLAlchemy-модели для пользователей.
- Enum UserRole: роли пользователя (права доступа)
- Модель Users: пользователь с email, паролем, ролью и связью с бронированиями.
- Использует TYPE_CHECKING для IDE-подсказок relationship.
"""

from enum import Enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Импорт только для типов (не вызывает циклический импорт)
    from app.bookings.models import Bookings

class UserRole(Enum):
    """
    Перечисление ролей пользователей:
    - USER: обычный пользователь
    - DEVELOPER: разработчик (расширенные права)
    - ADMIN: администратор (максимальные права)
    """
    USER = "Пользователь"
    DEVELOPER = "Разработчик"
    ADMIN = "Администратор"

class Users(Base):
    """
    SQLAlchemy-модель пользователя (таблица 'users').

    Атрибуты:
        id: int — идентификатор пользователя (PK)
        email: str — email (уникальный, но ограничение на уровне БД)
        hashed_password: str — хешированный пароль
        role: UserRole — роль пользователя (enum)
        bookings: list["Bookings"] — связь: все бронирования пользователя
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)  # unique=True желательно в миграции
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole),
        nullable=False,
        default=UserRole.USER
    )

    # Связь: все бронирования пользователя (из app.bookings.models)
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        """Удобное строковое представление пользователя для логов/admin."""
        return f"Пользователь {self.email} с ролью {self.role.value}"
