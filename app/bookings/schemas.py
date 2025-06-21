"""
Pydantic-схемы для операций с бронированиями.

- SBooking: базовая информация о брони (используется для вывода в списках).
- SBookingInfo: расширенная схема с деталями по комнате (для отображения пользователю).
- SNewBooking: данные для создания новой брони (для POST-запросов).
- Все схемы используют from_attributes=True для поддержки конвертации из ORM-моделей.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SBooking(BaseModel):
    """
    Базовая информация о бронировании (отдается пользователю).

    Атрибуты:
        id: int — ID бронирования
        room_id: int — ID комнаты
        user_id: int — ID пользователя
        date_from: date — дата заезда
        date_to: date — дата выезда
        price: int — цена за ночь
        total_cost: int — итоговая сумма бронирования
        total_days: int — количество дней

    Применяется при выводе списка/деталей бронирований.
    """
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)  # Позволяет конвертировать ORM-модели напрямую


class SBookingInfo(SBooking):
    """
    Расширенная информация о бронировании с деталями по номеру.

    Дополнительные поля:
        image_id: int — ID изображения комнаты
        name: str — название номера
        description: Optional[str] — описание номера
        services: list[str] — список услуг, предоставляемых в номере

    Используется для подробного отображения информации о брони.
    """
    image_id: int               # ID изображения комнаты
    name: str                   # Название номера
    description: Optional[str]  # Описание комнаты (может отсутствовать)
    services: list[str]         # Список услуг (Wi-Fi, завтрак и др.)

    model_config = ConfigDict(from_attributes=True)


class SNewBooking(BaseModel):
    """
    Данные для создания новой брони.

    Поля:
        room_id: int — ID комнаты
        date_from: date — дата заезда
        date_to: date — дата выезда

    Используется при создании бронирования (POST /bookings).
    """
    room_id: int
    date_from: date
    date_to: date

    model_config = ConfigDict(from_attributes=True)
