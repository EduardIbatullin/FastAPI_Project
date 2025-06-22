"""
Роутер FastAPI для работы с отелями:
- Поиск отелей по локации и датам (GET /hotels/{location})
- Получение информации об отеле по id (GET /hotels/id/{hotel_id})

Используется кеширование через fastapi-cache2 (60 сек) — компромисс между актуальностью и скоростью.
В демо-режиме искусственная задержка (3 сек), чтобы продемонстрировать работу кеша.
"""

import asyncio
from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    """
    Получает список всех отелей по локации, где есть свободные номера на указанные даты.

    :param location: Город или регион (поиск по подстроке, нечувствительно к регистру)
    :param date_from: Дата заезда (YYYY-MM-DD)
    :param date_to: Дата выезда (YYYY-MM-DD)
    :return: Список SHotelInfo (отели с полем rooms_left)
    :raises DateFromCannotBeAfterDateTo: если дата заезда позже даты выезда

    ⚠️ Используется кеш 60 сек и искусственная задержка (3 сек) для демонстрации.
    """
    await asyncio.sleep(3)  # Искуственная задержка для демонстрации кеша
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
@cache(expire=60)
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    """
    Получает информацию об отеле по его id.

    :param hotel_id: id отеля
    :return: SHotel (данные отеля) или None, если не найден
    """
    return await HotelDAO.find_one_or_none(id=hotel_id)
