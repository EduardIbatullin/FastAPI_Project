from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        """
        Получает список **всех номеров** отеля, включая занятые, с расчетом стоимости.
        """

        """
        WITH booked_rooms AS (
            SELECT 
                room_id, 
                COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE 
                date_to >= '2023-05-15'
                AND date_from <= '2023-06-20'
            GROUP BY room_id
        )
        SELECT 
            r.id, 
            r.hotel_id, 
            r.name, 
            r.description, 
            r.services, 
            r.price, 
            r.quantity, 
            r.image_id,
            (r.price * ('2023-06-20'::DATE - '2023-05-15'::DATE)) AS total_cost, -- Стоимость бронирования
            GREATEST(r.quantity - COALESCE(br.rooms_booked, 0), 0) AS rooms_left -- Оставшиеся номера
        FROM rooms r
        LEFT JOIN booked_rooms br ON br.room_id = r.id
        WHERE r.hotel_id = 1;
        """


        # Подсчет забронированных номеров
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .where(
                and_(
                    Bookings.date_to >= date_from,
                    Bookings.date_from <= date_to,
                )
            )
            .select_from(Bookings)
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        # Запрос на выборку всех номеров отеля
        get_rooms = (
            select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),  # Стоимость бронирования
                func.greatest(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0), 0).label("rooms_left"),  # Оставшиеся номера
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)  # LEFT JOIN, чтобы не терять номера без бронирований
            .where(Rooms.hotel_id == hotel_id)  # Фильтр по конкретному отелю
        )

        async with async_session_maker() as session:
            rooms = await session.execute(get_rooms)
            rooms_data = rooms.mappings().all()
            logger.warning(f"📦 Result count: {len(rooms_data)}")
            return rooms_data
        
    @classmethod
    async def find_available(cls, hotel_id: int, date_from: date, date_to: date):
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .where(
                and_(
                    Bookings.date_to >= date_from,
                    Bookings.date_from <= date_to,
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        rooms_left_expr = func.greatest(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0), 0)

        query = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
                rooms_left_expr.label("rooms_left"),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(
                and_(
                    Rooms.hotel_id == hotel_id,
                    rooms_left_expr > 0,
                )
            )
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()


