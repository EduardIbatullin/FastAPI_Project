from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_optional_user

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
async def login_form(request: Request, user=Depends(get_optional_user)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@router.post("/auth/login")
async def login_process(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    user = await authenticate_user(email=email, password=password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверные email или пароль",
            "user": None,
        })

    access_token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url="/pages/hotels", status_code=status.HTTP_302_FOUND)
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return response


@router.get("/register")
async def register_form(request: Request, user=Depends(get_optional_user)):
    return templates.TemplateResponse("register.html", {"request": request, "user": user})


@router.post("/auth/register")
async def register_process(
    request: Request,
    email: str = Form(...),
    name: str = Form(...),
    password: str = Form(...),
):
    existing_user = await UsersDAO.find_one_or_none(email=email)
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь с таким email уже зарегистрирован",
            "user": None,
        })

    hashed_password = get_password_hash(password)
    await UsersDAO.add(email=email, name=name, hashed_password=hashed_password)

    response = RedirectResponse(url="/pages/login", status_code=status.HTTP_302_FOUND)
    return response

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/pages/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("booking_access_token")
    return response
