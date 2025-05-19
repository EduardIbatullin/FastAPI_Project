from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.users.dependencies import get_optional_user

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels/{hotel_id}")
async def hotel_detail(
    request: Request,
    hotel_id: int,
    date_from: str = Query(...),
    date_to: str = Query(...),
    user=Depends(get_optional_user),
):
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)

    return templates.TemplateResponse("hotel_detail.html", {
        "request": request,
        "user": user,
        "hotel": hotel,
        "rooms": rooms,
        "date_from": date_from,
        "date_to": date_to,
    })
