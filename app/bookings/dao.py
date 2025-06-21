"""
DAO для работы с бронированиями:
- Получение всех бронирований пользователя.
- Добавление новой брони с проверкой дат и количества доступных мест.
- Логирование ошибок через logger.
"""

from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    """
    Data Access Object для сущности Bookings.

    Реализует поиск и создание бронирований с учётом доступности номеров.
    """
    model = Bookings

    @classmethod
    async def find_all(cls, user_id: int) -> list:
        """
        Получает список всех бронирований пользователя с информацией о номерах.

        :param user_id: ID пользователя
        :return: Список бронирований (dict с полями Bookings и Rooms)
        """
        # СЫРОЙ SQL:
        # SELECT
        #     b.room_id,
        #     b.user_id,
        #     b.date_from,
        #     b.date_to,
        #     b.price,
        #     b.total_cost,
        #     b.total_days,
        #     r.image_id,
        #     r.name,
        #     r.description,
        #     r.services
        # FROM bookings b
        # JOIN rooms r ON b.room_id = r.id
        # WHERE b.user_id = :user_id;

        get_bookings = (
            select(
                Bookings.__table__.columns,
                Rooms.__table__.columns,
            )
            .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
            .where(Bookings.user_id == user_id)
        )
        async with async_session_maker() as session:
            bookings = await session.execute(get_bookings)
            return bookings.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> Bookings | None:
        """
        Пытается создать новую бронь для комнаты на выбранные даты.

        Логика:
        - Считает количество занятых мест по room_id и датам (через CTE booked_rooms).
        - Если есть свободные места — создаёт бронирование, иначе возвращает None.

        :param user_id: ID пользователя
        :param room_id: ID комнаты
        :param date_from: дата заезда
        :param date_to: дата выезда
        :return: Объект Bookings или None (если мест нет)
        """
        # СЫРОЙ SQL:
        # WITH booked_rooms AS (
        #     SELECT * FROM bookings
        #     WHERE room_id = :room_id
        #       AND date_from <= :date_to
        #       AND date_to >= :date_from
        # )
        # SELECT rooms.quantity - COUNT(booked_rooms.room_id) AS rooms_left
        # FROM rooms
        # LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        # WHERE rooms.id = :room_id
        # GROUP BY rooms.quantity, booked_rooms.room_id

        try:
            async with async_session_maker() as session:
                # CTE: ищет все пересекающиеся бронирования по датам
                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == room_id,
                        and_(
                            Bookings.date_to >= date_from,
                            Bookings.date_from <= date_to
                        )
                    )
                ).cte("booked_rooms")

                # Считает оставшееся количество свободных мест
                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    # Узнаём цену комнаты
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()

                    # Добавляем новую бронь
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).returning(Bookings)

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except SQLAlchemyError:
            logger.exception(
                "Database Exc: Cannot add booking",
                extra={
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                },
            )
        except Exception:
            logger.exception(
                "Unknown Exc: Cannot add booking",
                extra={
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                },
            )
