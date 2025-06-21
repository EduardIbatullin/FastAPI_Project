"""
SQLAdmin: административные представления для моделей пользователей, отелей, комнат и бронирований.

- Определяет наборы полей, фильтров, лейблов и иконок для каждой сущности.
- Реализует защиту от удаления пользователей.
- Настраивает видимость, доступность и визуализацию данных в админке.
"""

from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    """
    Админ-представление для пользователей.

    Особенности:
    - Скрыт пароль (hashed_password) из детального и формы.
    - Нельзя удалить пользователя (can_delete = False).
    - Иконка: пользователь.
    """
    # --- Отображаемые колонки и фильтры ---
    column_list = [Users.id, Users.email, Users.role, Users.bookings]
    column_details_exclude_list = [Users.hashed_password]
    column_labels = {
        Users.email: "Почта",
        Users.role: "Роль",
        Users.bookings: "Бронирования"
    }
    column_searchable_list = [Users.email]
    # --- Настройки формы ---
    form_excluded_columns = [Users.hashed_password]
    form_widget_args = {
        Users.id: {"readonly": True},
    }
    # --- Визуальные настройки и защита ---
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"  # Для меню SQLAdmin (FontAwesome)
    can_delete = False  # Защита от случайного удаления


class HotelsAdmin(ModelView, model=Hotels):
    """
    Админ-представление для отелей.

    Особенности:
    - Выводит все поля из таблицы Hotels + rooms (список комнат).
    - Иконка: отель.
    """
    # В column_list попадают все поля модели Hotels + реляция rooms
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
    icon = "fa-solid fa-hotel"  # Иконка отеля


class RoomsAdmin(ModelView, model=Rooms):
    """
    Админ-представление для комнат.

    Особенности:
    - Отображает все поля комнаты + реляции hotel, bookings.
    - Иконка: кровать.
    """
    # В column_list попадают все поля модели Rooms + hotel и bookings (реляции)
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
    icon = "fa-solid fa-bed"  # Иконка номера


class BookingsAdmin(ModelView, model=Bookings):
    """
    Админ-представление для бронирований.

    Особенности:
    - Фильтрация по комнате и датам.
    - Скрыты итого и количество дней из формы (только для чтения).
    - Иконка: книга.
    """
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
    # Исключаем из формы вычисляемые поля
    form_excluded_columns = [Bookings.total_cost, Bookings.total_days]
    form_widget_args = {
        Bookings.id: {"readonly": True},
    }
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"  # Иконка бронирования
