"""
Интеграционный тест DAO слоя бронирований.
Проверяет:
- успешное добавление новой брони через BookingDAO
- корректность полей (user_id, room_id, даты)
- получение той же записи из БД по id
"""

from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO

@pytest.mark.asyncio
async def test_add_and_get_booking():
    """
    Создаёт бронирование и проверяет его сохранение в базе.
    Предполагается, что user_id=2 и room_id=2 есть в тестовых фикстурах.
    """
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking is not None
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2
    assert new_booking.date_from == datetime(2023, 7, 10)
    assert new_booking.date_to == datetime(2023, 7, 24)

    booking_from_db = await BookingDAO.find_by_id(new_booking.id)
    assert booking_from_db is not None
    assert booking_from_db.id == new_booking.id
