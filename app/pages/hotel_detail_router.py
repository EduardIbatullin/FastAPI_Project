from datetime import date, timedelta

from fastapi import APIRouter, Request, Depends, Query
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.users.dependencies import get_optional_user

from app.logger import logger

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels/{hotel_id}")
async def hotel_detail(
    request: Request,
    hotel_id: int,
    date_from: date = Query(...),
    date_to: date = Query(...),
    user=Depends(get_optional_user),
):
    today = date.today()
    tomorrow = today + timedelta(days=1)

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

    return templates.TemplateResponse("hotel_detail.html", {
        "request": request,
        "user": user,
        "hotel": hotel,
        "rooms": rooms,
        "date_from": date_from,
        "date_to": date_to,
    })
