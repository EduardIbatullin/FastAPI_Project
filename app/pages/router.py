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


@router.get("")
async def index_page(
    request: Request,
    location: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    user=Depends(get_optional_user),
):
    today = date.today()

    def parse_date(value: Optional[str]) -> date:
        try:
            return date.fromisoformat(value) if value else today
        except ValueError:
            return today

    parsed_from = parse_date(date_from)
    parsed_to = parse_date(date_to)

    if not location:
        hotels = await HotelDAO.find_all("", today, today)
    elif location and not date_from and not date_to:
        hotels = await HotelDAO.find_all(location, today, today)
    else:
        hotels = await HotelDAO.find_all(location, max(parsed_from, today), parsed_to)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "hotels": hotels,
        "location": location,
        "date_from": parsed_from,
        "date_to": parsed_to,
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
