from datetime import date

from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.users.dependencies import get_optional_user

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_pages(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time),
    user=Depends(get_optional_user),
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels, "user": user},
    )


from datetime import date
from typing import Optional
from fastapi import Request, APIRouter, Query, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.dao import HotelDAO
from app.users.dependencies import get_optional_user

router = APIRouter(prefix="/pages", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


from datetime import date, timedelta

from datetime import date, timedelta

@router.get("")
async def index_page(
    request: Request,
    location: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    user=Depends(get_optional_user),
):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    def parse_date(value: Optional[str], default: date) -> date:
        try:
            return date.fromisoformat(value) if value else default
        except ValueError:
            return default

    parsed_from = parse_date(date_from, today)
    parsed_to = parse_date(date_to, tomorrow)

    # ⛔ Автокоррекция дат
    if parsed_from < today:
        parsed_from = today
    if parsed_to <= today:
        parsed_to = tomorrow

    # ❌ Проверка логики
    error = None
    if parsed_to <= parsed_from:
        error = "Дата выезда должна быть позже даты заезда хотя бы на 1 день"
        hotels = []
    else:
        hotels = await HotelDAO.find_all(
            location or "", parsed_from, parsed_to
        )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "hotels": hotels,
        "location": location,
        "date_from": parsed_from,
        "date_to": parsed_to,
        "error": error,
    })


# @router.get("/hotels/{hotel_id}")
# async def get_hotel_with_rooms(
#     hotel_id: int,
#     request: Request,
#     user=Depends(get_optional_user),
# ):
#     today = date.today()
#     hotel = await HotelDAO.find_by_id(hotel_id)
#     rooms = await RoomDAO.find_available(hotel_id, today, today)
#     return templates.TemplateResponse("hotel_detail.html", {
#         "request": request,
#         "hotel": hotel,
#         "rooms": rooms,
#         "user": user,
#     })
