"""
Роутер для операций с бронированиями:
- Получить список своих броней (GET /bookings)
- Добавить новое бронирование (POST /bookings)
- Удалить бронирование (DELETE /bookings/{booking_id})
Все операции требуют аутентификации пользователя.
"""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.bookings.service import BookingsService
# from app.tasks.tasks import send_booking_confirmation_email  # Отключено для тестов/демо
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookingInfo]:
    """
    Получает список всех бронирований пользователя.

    Требуется аутентификация.
    :return: Список объектов SBookingInfo (ваши бронирования)
    """
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
) -> SBookingInfo:
    """
    Добавляет новое бронирование для текущего пользователя.

    :param booking: Данные для новой брони
    :param user: Текущий пользователь (автоматически из Depends)
    :return: Информация о созданной брони (SBookingInfo)
    """
    new_booking = await BookingsService.add_booking(booking, user)
    # Отправка email-уведомления временно отключена (для тестов/демо)
    # send_booking_confirmation_email.delay(new_booking, user.email)
    return new_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user)
) -> None:
    """
    Удаляет бронирование пользователя по id.

    Возвращает 204 No Content. Требуется аутентификация.
    """
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
