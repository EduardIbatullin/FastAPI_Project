from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.role, Users.bookings]
    column_details_exclude_list = [Users.hashed_password]
    column_labels = {
        Users.email: "Почта",
        Users.role: "Роль",
        Users.bookings: "Бронирования"
    }
    column_searchable_list = [Users.email]
    form_excluded_columns = [Users.hashed_password]
    form_widget_args = {
        Users.id: {"readonly": True},
    }
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_delete = False


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    column_labels = {
        Hotels.name: "Название",
        Hotels.location: "Расположение",
        Hotels.services: "Услуги",
        Hotels.rooms_quantity: "Кол-во номеров",
        Hotels.rooms: "Номера",
    }
    form_widget_args = {
        Hotels.id: {"readonly": True},
    }
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    column_labels = {
        Rooms.name: "Название",
        Rooms.description: "Описание",
        Rooms.price: "Цена",
        Rooms.services: "Услуги",
        Rooms.quantity: "Количество",
        Rooms.hotel: "Отель",
        Rooms.bookings: "Бронирования",
    }
    form_widget_args = {
        Rooms.id: {"readonly": True},
    }
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [
        Bookings.id,
        Bookings.user,
        Bookings.room,
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
        Bookings.total_cost,
        Bookings.total_days,
    ]

    column_labels = {
        Bookings.user: "Пользователь",
        Bookings.room: "Номер",
        Bookings.date_from: "Дата заезда",
        Bookings.date_to: "Дата выезда",
        Bookings.price: "Цена/день",
        Bookings.total_cost: "Итого",
        Bookings.total_days: "Кол-во дней",
    }

    column_filters = [Bookings.room, Bookings.date_from, Bookings.date_to]
    form_excluded_columns = [Bookings.total_cost, Bookings.total_days]
    form_widget_args = {
        Bookings.id: {"readonly": True},
    }
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
