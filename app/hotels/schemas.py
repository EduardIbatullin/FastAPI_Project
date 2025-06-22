"""
Pydantic-схемы для работы с объектами отелей.

- SHotel: базовая схема отеля (для большинства запросов и выдачи по id)
- SHotelInfo: расширенная схема с полем rooms_left (выдаётся при поиске отелей с фильтрацией по датам)
"""

from typing import List

from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    """
    Базовая схема отеля.

    Атрибуты:
        id: int — идентификатор отеля (primary key)
        name: str — название отеля
        location: str — город или адрес
        services: List[str] — список предоставляемых услуг (JSON), например ["Wi-Fi", "Парковка"]
        rooms_quantity: int — сколько всего комнат в отеле
        image_id: int — идентификатор картинки (для превью/галереи)
    """
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)  # ORM-mode, можно возвращать напрямую из моделей


class SHotelInfo(SHotel):
    """
    Расширенная схема отеля для поиска по датам.

    Добавляет:
        rooms_left: int — количество свободных комнат на указанный период поиска (выдаётся в поиске /hotels/{location})
    """
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
