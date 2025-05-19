from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time
from app.hotels.dao import HotelDAO
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

@router.get("")
async def index_page(
    request: Request,
    user=Depends(get_optional_user),
):
    hotels = await HotelDAO.get_all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "hotels": hotels,
    })

