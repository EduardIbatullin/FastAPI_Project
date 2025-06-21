"""
Модель SQLAlchemy для бронирований номеров.

- Связывает пользователя, комнату, даты и цену бронирования.
- total_cost и total_days рассчитываются автоматически (через Computed).
- Поддерживает связи user <-> bookings, room <-> bookings для ORM.
"""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Для автодополнения и проверки типов в IDE (не влияет на runtime)
    from app.hotels.rooms.models import Rooms
    from app.users.models import Users


class Bookings(Base):
    """
    Модель таблицы bookings (брони номеров отеля).

    Основные поля:
        - room_id, user_id: внешние ключи на комнату и пользователя
        - date_from, date_to: период бронирования
        - price: стоимость одной ночи
        - total_cost: итоговая сумма брони (вычисляется, Computed)
        - total_days: длительность в днях (вычисляется, Computed)
    """
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    # total_cost: итоговая стоимость бронирования (автоматически, на стороне БД)
    # Используется SQLAlchemy Computed для авторасчёта в запросах SELECT/INSERT
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))

    # total_days: количество дней бронирования (автоматически, Computed)
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    # ORM-связи
    user: Mapped["Users"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship(back_populates="bookings")

    def __str__(self) -> str:
        """Строковое представление брони для отладки и админки."""
        return f"Бронь #{self.id}"
