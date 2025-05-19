from datetime import date
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.users.dependencies import get_current_user
from app.bookings.dao import BookingDAO

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/booking")
async def booking_form(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("booking.html", {
        "request": request,
        "user": user,
    })


@router.post("/booking")
async def booking_submit(
    request: Request,
    room_id: int = Form(...),
    date_from: date = Form(...),
    date_to: date = Form(...),
    user=Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )

    if not booking:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "error": "Нет свободных номеров на выбранные даты."
        })

    return RedirectResponse(url="/pages/profile", status_code=status.HTTP_302_FOUND)
