"""
Роутер FastAPI для HTML-страниц фронта (через Jinja2).

Отвечает за рендеринг главной страницы поиска, отображение списка отелей и передачу переменных из backend в шаблоны.
Все параметры (location, даты) приходят через query string.
"""

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time
from app.hotels.dao import HotelDAO
from app.users.dependencies import get_optional_user

router = APIRouter(prefix="/pages", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def index_page(
    request: Request,
    location: Optional[str] = Query(None, description="Локация для поиска отеля (город или регион)"),
    date_from: Optional[str] = Query(None, description="Дата заезда в формате YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="Дата выезда в формате YYYY-MM-DD"),
    user=Depends(get_optional_user),
):
    """
    Главная страница поиска отелей (выбор локации и дат).

    :param request: FastAPI Request (обязательно для шаблонов)
    :param location: str | None — поисковый город/регион (query param)
    :param date_from: str | None — дата заезда (query param, ISO format)
    :param date_to: str | None — дата выезда (query param, ISO format)
    :param user: опциональный пользователь (Depends)
    :return: HTML шаблон index.html с переменными поиска, ошибкой (если даты невалидны), списком найденных отелей
    """
    today = date.today()
    tomorrow = today + timedelta(days=1)

    def parse_date(value: Optional[str], default: date) -> date:
        try:
            return date.fromisoformat(value) if value else default
        except ValueError:
            return default

    parsed_from = parse_date(date_from, today)
    parsed_to = parse_date(date_to, tomorrow)

    # Валидируем: нельзя выбрать дату из прошлого и выезд не раньше заезда
    if parsed_from < today:
        parsed_from = today
    if parsed_to <= today:
        parsed_to = tomorrow

    error = None
    if parsed_to <= parsed_from:
        error = "Дата выезда должна быть позже даты заезда хотя бы на 1 день"
        hotels = []
    else:
        hotels = await HotelDAO.find_all(location or "", parsed_from, parsed_to)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "hotels": hotels,
        "location": location,
        "date_from": parsed_from,
        "date_to": parsed_to,
        "error": error,
    })


@router.get("/hotels")
async def get_hotels_pages(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time),
    user=Depends(get_optional_user),
):
    """
    Страница со списком найденных отелей.

    :param request: FastAPI Request (обязательно для шаблонов)
    :param hotels: список отелей (получен через Depends)
    :param user: текущий пользователь (опционально)
    :return: HTML шаблон hotels.html с переданными данными
    """
    return templates.TemplateResponse("hotels.html", {
        "request": request,
        "hotels": hotels,
        "user": user,
    })
