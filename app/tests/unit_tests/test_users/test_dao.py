"""
Юнит-тест для метода UsersDAO.find_by_id.
Проверяет:
- Что существующие пользователи корректно находятся
- Что несуществующий ID возвращает None
"""

import pytest
from app.users.dao import UsersDAO

@pytest.mark.parametrize("user_id,email,exist", [
    (1, "test@test.com", True),       # пользователь с таким ID есть в тестовой БД
    (2, "artem@example.com", True),   # ещё один валидный ID
    (999, "noone@example.com", False) # ID отсутствует
])
async def test_find_user_by_id(user_id, email, exist):
    """
    Проверяет UsersDAO.find_by_id:
    - при существующем ID возвращает пользователя с ожидаемым email
    - при несуществующем ID — None
    """
    user = await UsersDAO.find_by_id(user_id)
    if exist:
        assert user is not None
        assert user.id == user_id
        assert user.email == email
        assert hasattr(user, "email")
    else:
        assert user is None
