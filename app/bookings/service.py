"""
Сервисный слой для работы с бронированиями.

- Инкапсулирует бизнес-логику для бронирований поверх DAO.
- Выполняет дополнительную валидацию и обработку ошибок.
- Возвращает валидированные данные для API.
"""

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBookedException
from app.users.models import Users


class BookingsService:
    """
    Сервис для работы с бронированиями.

    Зачем нужен:
    - DAO занимается только работой с БД.
    - Service-слой — логика, валидация, обработка ошибок, возврат схем для API.
    """

    @classmethod
    async def add_booking(
        cls,
        booking: SNewBooking,
        user: Users,
    ) -> SBooking:
        """
        Добавляет новое бронирование для пользователя через DAO.

        :param booking: Схема с параметрами новой брони (room_id, date_from, date_to)
        :param user: Модель текущего пользователя (Users)
        :raises RoomCannotBeBookedException: Если нет доступных мест/ошибка бронирования
        :return: Объект SBooking (валидированные данные бронирования)
        """
        db_booking = await BookingDAO.add(
            user.id,
            booking.room_id,
            booking.date_from,
            booking.date_to,
        )
        if not db_booking:
            raise RoomCannotBeBookedException
        return SBooking.model_validate(db_booking)
