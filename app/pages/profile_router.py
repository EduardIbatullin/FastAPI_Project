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
    bookings = await BookingDAO.find_all(user_id=user.id)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "bookings": bookings,
    })
