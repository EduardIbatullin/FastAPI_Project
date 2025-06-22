"""
Интеграционные тесты API авторизации и регистрации.
Проверяет:
- Регистрацию нового пользователя
- Обработку повторной регистрации
- Аутентификацию (включая неверные данные)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 200),    # Новый пользователь
    ("kot@pes.com", "kot0pes", 409),    # Повторная регистрация
    ("pes@kot.com", "pesokot", 200),    # Новый пользователь
    ("abcdef", "kotopes", 422),         # Невалидный email
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    """
    Проверка регистрации пользователей с различными входными данными.
    Проверяется статус-код:
    - 200 — регистрация успешна
    - 409 — пользователь уже существует
    - 422 — невалидный формат email
    """
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),                   # Успешный логин
    ("artem@example.com", "artem", 200),              # Успешный логин
    ("nonexistent@example.com", "password", 401),     # Не существует
    ("test@test.com", "wrongpassword", 401),          # Неверный пароль
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    """
    Проверка логина с корректными и некорректными данными.
    Проверяется статус-код:
    - 200 — успешная авторизация
    - 401 — неверные данные
    """
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code
