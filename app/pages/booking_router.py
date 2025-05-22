from datetime import date, timedelta

from fastapi import APIRouter, Request, Form, Depends, Query, status
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
async def booking_form(
    request: Request,
    room_id: int = Query(...),
    date_from: date = Query(...),
    date_to: date = Query(...),
    user=Depends(get_current_user),
):
    return templates.TemplateResponse("booking.html", {
        "request": request,
        "user": user,
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })


@router.post("/booking")
async def booking_submit(
    request: Request,
    room_id: int = Form(...),
    date_from: date = Form(...),
    date_to: date = Form(...),
    user=Depends(get_current_user),
):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    formatted_today = today.strftime("%d-%m-%Y")
    formatted_tomorrow = tomorrow.strftime("%d-%m-%Y")

    # ❌ Проверка: заезд в прошлом
    if date_from < today:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": f"Дата заезда не может быть ранее {formatted_today}"
        })

    # ❌ Проверка: выезд раньше, чем завтра
    if date_to < tomorrow:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": f"Дата выезда не может быть ранее {formatted_tomorrow}"
        })

    # ❌ Проверка: выезд в тот же день или раньше заезда
    if date_to <= date_from:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": "Дата выезда должна быть позже даты заезда хотя бы на 1 день."
        })

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
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": "Нет свободных номеров на выбранные даты."
        })

    return RedirectResponse(url="/pages/profile", status_code=status.HTTP_302_FOUND)


@router.post("/bookings/{booking_id}/delete")
async def delete_booking_from_profile(booking_id: int, user=Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
    return RedirectResponse(url="/pages/profile", status_code=303)