"""
Pydantic-схемы для работы с комнатами (rooms) в API.

SRoom     — базовая схема комнаты (описание, услуги, цена и пр.)
SRoomInfo — расширенная схема для ответа API (добавляет стоимость за период и кол-во свободных мест).
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    """
    Базовая схема комнаты для выдачи в API и автодокументации.

    Атрибуты:
        id: int                — идентификатор комнаты (primary key)
        hotel_id: int          — идентификатор отеля, к которому принадлежит комната
        name: str              — название комнаты (например, "Люкс")
        description: str | None— описание (nullable)
        services: list[str]    — список предоставляемых услуг (JSON), например ["Wi-Fi", "Парковка"]
        price: int             — цена за ночь (₽)
        quantity: int          — сколько таких комнат в отеле всего
        image_id: int          — id картинки для превью/галереи

    Все поля соответствуют ORM-модели Rooms.
    """
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: List[str]
    price: int
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)  # позволяет преобразовать ORM в Pydantic-схему


class SRoomInfo(SRoom):
    """
    Расширенная схема комнаты для ответа API.

    Добавляет к базовой:
        total_cost: int  — итоговая стоимость бронирования за выбранный период (например, 3 ночи * цена)
        rooms_left: int  — число свободных мест этой категории в указанный период

    Используется в эндпоинтах, возвращающих список комнат с учётом дат и доступности.
    """
    total_cost: int        # Стоимость за выбранный период (дней)
    rooms_left: int        # Сколько осталось свободных комнат

    model_config = ConfigDict(from_attributes=True)
