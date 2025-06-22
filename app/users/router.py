"""
Роутер FastAPI для операций с пользователями и аутентификацией:
- Регистрация (POST /auth/register)
- Логин (POST /auth/login)
- Логаут (POST /auth/logout)
- Получение информации о себе (GET /auth/me)
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserOut

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserAuth) -> None:
    """
    Регистрирует нового пользователя.

    :param user_data: Данные для регистрации (email и пароль, схема SUserAuth)
    :raises UserAlreadyExistsException: если пользователь с таким email уже существует
    :return: None (статус 201 Created)
    """
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(response: Response, user_data: SUserAuth) -> str:
    """
    Аутентифицирует пользователя по email и паролю.

    :param user_data: email и пароль (схема SUserAuth)
    :param response: HTTP Response для установки cookie
    :raises IncorrectEmailOrPasswordException: если пользователь не найден или пароль неверный
    :return: JWT access_token (и устанавливает его в httpOnly cookie)
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="booking_access_token",
        value=access_token,
        httponly=True,
        samesite="lax"
    )
    return access_token


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response) -> dict:
    """
    Логаут: удаляет cookie с access_token.

    :param response: HTTP Response для удаления cookie
    :return: {"detail": "..."}
    """
    response.delete_cookie(key="booking_access_token")
    return {"detail": "User logged out successfully"}


@router.get("/me", response_model=SUserOut, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: Users = Depends(get_current_user)) -> SUserOut:
    """
    Возвращает информацию о текущем авторизованном пользователе.

    :param current_user: модель пользователя, полученная через Depends(get_current_user)
    :return: схема SUserOut (данные пользователя)
    """
    return current_user
