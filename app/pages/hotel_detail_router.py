"""
Роутер страницы "Детали отеля" для фронта.
- Отдаёт шаблон hotel_detail.html с информацией об отеле и всех его номерах на выбранные даты.
- Валидирует даты, возвращает 400 (Bad Request) при ошибке.
"""

from datetime import date, timedelta

from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.users.dependencies import get_optional_user

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels/{hotel_id}")
async def hotel_detail(
    request: Request,
    hotel_id: int,
    date_from: date = Query(..., description="Дата заезда (YYYY-MM-DD)"),
    date_to: date = Query(..., description="Дата выезда (YYYY-MM-DD)"),
    user=Depends(get_optional_user),
):
    """
    Детальная страница отеля (GET /pages/hotels/{hotel_id}):
    - Показывает карточку отеля, список всех комнат и их доступность на выбранные даты.
    - В шаблон передаются: hotel, rooms, user, date_from, date_to.
    :param request: FastAPI Request
    :param hotel_id: id отеля
    :param date_from: дата заезда
    :param date_to: дата выезда
    :param user: неавторизованный пользователь (для навигации и шаблона)
    :raises HTTPException 400: если даты некорректны
    :return: TemplateResponse с hotel_detail.html и параметрами
    """
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Проверки на корректность дат бронирования
    if date_from < today:
        raise HTTPException(
            status_code=400,
            detail=f"Дата заезда не может быть ранее {today.strftime('%d-%m-%Y')}"
        )

    if date_to < tomorrow:
        raise HTTPException(
            status_code=400,
            detail=f"Дата выезда не может быть ранее {tomorrow.strftime('%d-%m-%Y')}"
        )

    if date_to <= date_from:
        raise HTTPException(
            status_code=400,
            detail="Дата выезда должна быть позже даты заезда хотя бы на 1 день"
        )

    hotel = await HotelDAO.find_one_or_none(id=hotel_id)
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)

    # Если hotel == None, шаблон hotel_detail.html должен корректно отработать этот случай
    return templates.TemplateResponse("hotel_detail.html", {
        "request": request,
        "user": user,
        "hotel": hotel,
        "rooms": rooms,
        "date_from": date_from,
        "date_to": date_to,
    })
