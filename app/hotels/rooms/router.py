"""
Роутер FastAPI для операций с комнатами отеля.

Позволяет получить список всех комнат по отелю с расчетом свободных мест и стоимости за период.
"""

from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query, HTTPException
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
@cache(expire=3)
async def get_rooms_by_date(
    hotel_id: int,
    date_from: date = Query(..., description=f"Дата заезда, например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Дата выезда, например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SRoomInfo]:
    """
    Получить список всех комнат отеля на указанный период.

    :param hotel_id: ID отеля
    :param date_from: Дата заезда (YYYY-MM-DD)
    :param date_to: Дата выезда (YYYY-MM-DD)
    :return: Список комнат (SRoomInfo), для каждой — количество свободных мест (rooms_left) и итоговая стоимость (total_cost)
    :raises HTTPException 400: если date_from > date_to

    Пример ответа:
        [
            {
                "id": 1,
                "hotel_id": 3,
                "name": "Стандарт",
                "price": 3700,
                "quantity": 2,
                "rooms_left": 1,
                "total_cost": 7400,
                ...
            }
        ]
    """
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="Дата заезда не может быть позже даты выезда")

    return await RoomDAO.find_all(hotel_id, date_from, date_to)
