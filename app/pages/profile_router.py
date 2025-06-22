"""
Роутер для страницы профиля пользователя ("/pages/profile").
Требует авторизацию, отображает все бронирования пользователя.
Если бронирований нет — в шаблон передаётся пустой список bookings.
"""

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.users.dependencies import get_current_user
from app.bookings.dao import BookingDAO

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
async def profile_page(
    request: Request,
    user=Depends(get_current_user),
):
    """
    Страница профиля пользователя.
    Требует авторизацию через Depends(get_current_user).
    В шаблон передаются:
      - request: FastAPI Request (для работы Jinja2)
      - user: объект текущего пользователя
      - bookings: список бронирований пользователя (может быть пустым)
    Если бронирований нет, bookings=[].
    """
    bookings = await BookingDAO.find_all(user_id=user.id)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "bookings": bookings,
    })
