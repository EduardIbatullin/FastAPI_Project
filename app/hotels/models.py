"""
Модель отеля для SQLAlchemy ORM.

Описывает структуру таблицы 'hotels' — основные поля, формат хранения услуг, связь с комнатами.
"""

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Импорт только для подсказок типов (чтобы PyCharm/VSCode понимали relationship)
    from hotels.rooms.models import Rooms


class Hotels(Base):
    """
    Модель таблицы 'hotels' (отели).

    Атрибуты:
        id: int — первичный ключ (идентификатор отеля)
        name: str — название отеля
        location: str — город, адрес или геолокация
        services: list[str] — список предоставляемых услуг (хранится как JSON в базе)
            Пример: ["Wi-Fi", "Парковка", "Завтрак"]
        rooms_quantity: int — общее количество комнат в отеле
        image_id: int — id изображения для превью или галереи
        rooms: list[Rooms] — список связанных комнат (relationship)
    """
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)           # Название отеля
    location: Mapped[str] = mapped_column(nullable=False)       # Город или адрес
    services: Mapped[list[str]] = mapped_column(JSON)           # JSON-список услуг (array of str)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False) # Сколько всего комнат в отеле
    image_id: Mapped[int]                                       # id изображения (внешняя связь, если есть)

    # ORM-связь: список комнат, относящихся к этому отелю
    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self) -> str:
        """
        Удобное строковое представление отеля для дебага и админки.
        """
        return f"Отель {self.name} {self.location[:30]}"
