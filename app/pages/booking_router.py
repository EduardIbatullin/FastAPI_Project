"""
Роутер для HTML-бронирования комнат через формы.
- Отображение и обработка формы бронирования (GET/POST)
- Проверка дат и отображение ошибок
- Удаление бронирования через профиль пользователя
"""

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
    room_id: int = Query(..., description="ID комнаты для бронирования"),
    date_from: date = Query(..., description="Дата заезда"),
    date_to: date = Query(..., description="Дата выезда"),
    user=Depends(get_current_user),
):
    """
    GET /pages/booking — форма бронирования комнаты.
    :param room_id: ID комнаты
    :param date_from: дата заезда
    :param date_to: дата выезда
    :param user: текущий пользователь (авторизация обязательна)
    :return: booking.html с исходными данными
    """
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
    """
    POST /pages/booking — обработка формы бронирования.
    Валидирует даты, создаёт бронирование. В случае ошибки — возвращает форму с ошибкой.
    :param room_id: ID комнаты
    :param date_from: дата заезда
    :param date_to: дата выезда
    :param user: текущий пользователь
    :return: booking.html (ошибка) или редирект на профиль (успех)
    """
    today = date.today()
    tomorrow = today + timedelta(days=1)
    formatted_today = today.strftime("%d-%m-%Y")
    formatted_tomorrow = tomorrow.strftime("%d-%m-%Y")

    # Проверка: заезд не раньше сегодня
    if date_from < today:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": f"Дата заезда не может быть ранее {formatted_today}"
        })

    # Проверка: выезд не раньше завтра
    if date_to < tomorrow:
        return templates.TemplateResponse("booking.html", {
            "request": request,
            "user": user,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
            "error": f"Дата выезда не может быть ранее {formatted_tomorrow}"
        })

    # Проверка: выезд позже заезда
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
    """
    POST /pages/bookings/{booking_id}/delete — удаляет бронирование пользователя по id.
    Проверяет владельца через user_id, после чего удаляет бронь.
    Редиректит обратно на страницу профиля.
    :param booking_id: id бронирования
    :param user: текущий пользователь
    :return: RedirectResponse на /pages/profile
    """
    await BookingDAO.delete(id=booking_id, user_id=user.id)
    return RedirectResponse(url="/pages/profile", status_code=303)
