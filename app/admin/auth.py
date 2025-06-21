"""
Кастомная аутентификация для админки SQLAdmin.

- Реализует вход/выход и проверку пользователя по JWT.
- Разрешён только доступ с ролью ADMIN или DEVELOPER.
- Все методы снабжены пояснениями и типами.
"""

from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.logger import logger

class AdminAuth(AuthenticationBackend):
    """
    Authentication backend для SQLAdmin.

    Методы:
    - login: авторизация по email и паролю, проверка роли, генерация access_token.
    - logout: выход, очистка сессии.
    - authenticate: проверка токена и прав, допуск только для ADMIN и DEVELOPER.
    """

    async def login(self, request: Request) -> bool:
        """
        Обработка формы логина администратора.
        Проверяет email и пароль пользователя, его роль, сохраняет токен в сессии.

        Returns:
            bool: True если пользователь авторизован, иначе False.
        """
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        # Логируем роль пользователя для отладки (но не используем print в production)
        if user is not None:
            logger.debug(f"Admin login attempt: user_id={user.id}, role={user.role.name}")
            if user.role.name in ("ADMIN", "DEVELOPER"):
                access_token = create_access_token({"sub": str(user.id)})
                request.session.update({"token": access_token})
                return True
        return False  # Явно возвращаем False, если не авторизован

    async def logout(self, request: Request) -> bool:
        """
        Очищает сессию пользователя (выход из админки).
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        """
        Проверяет валидность токена в сессии и права пользователя.
        Если нет токена или роль не ADMIN/DEVELOPER — редиректит на страницу логина.

        Returns:
            True если доступ разрешён, иначе RedirectResponse на форму логина.
        """
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)
        # Проверяем, что пользователь найден и его роль допустима для админки
        if not user or user.role.name not in ("ADMIN", "DEVELOPER"):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True

# Важно: secret_key должен быть вынесен в конфиг и загружаться из .env (см. app/config.py)
authentication_backend = AdminAuth(secret_key="...")  # Для production заменить на settings.SECRET_KEY
