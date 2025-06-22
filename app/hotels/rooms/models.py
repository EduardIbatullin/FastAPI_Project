"""
Модель SQLAlchemy для комнат отеля (rooms).
- Описывает структуру таблицы rooms и связи с отелями и бронями.
"""

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Для подсказок типов (чтобы IDE понимала связи)
    from app.bookings.models import Bookings
    from app.hotels.models import Hotels


class Rooms(Base):
    """
    Модель таблицы 'rooms' (комнаты отеля).

    Атрибуты:
        id: int — первичный ключ комнаты
        hotel_id: int — внешний ключ на отель
        name: str — название типа комнаты (например, "Стандарт", "Люкс")
        description: str | None — описание (nullable)
        price: int — цена за ночь
        services: list[str] | None — список предоставляемых услуг, хранится как JSON (nullable)
            Пример: ["Wi-Fi", "Кондиционер", "Завтрак"]
        quantity: int — количество одинаковых номеров данного типа
        image_id: int — id изображения комнаты (для галереи или превью)

        hotel: Hotels — связь с отелем (relationship, hotel.rooms)
        bookings: list[Bookings] — список бронирований (relationship, room.bookings)
    """

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)                   # Название типа комнаты (например, "Стандарт", "Люкс")
    description: Mapped[str] = mapped_column(nullable=True)             # Описание комнаты (опционально)
    price: Mapped[int] = mapped_column(nullable=False)                  # Цена за ночь
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)    # Список услуг (nullable, JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)               # Количество одинаковых номеров
    image_id: Mapped[int]                                               # id изображения (nullable не указан — уточните если нужно)

    # ORM-связи
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")      # Объект-отель, к которому принадлежит эта комната
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")  # Все бронирования этой комнаты

    def __str__(self) -> str:
        """
        Строковое представление комнаты для админки и отладки.
        """
        return f"Номер {self.name}"
