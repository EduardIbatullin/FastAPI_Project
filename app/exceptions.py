"""
Кастомные HTTP-исключения для бизнес-логики FastAPI-приложения.

- Все исключения наследуют от BookingException.
- Охватывают авторизацию, бронирование, работу с токеном, CSV, валидацию дат и пр.
- Используются для генерации осмысленных HTTP-ответов с нужным статусом и detail.
"""

from fastapi import HTTPException, status

class BookingException(HTTPException):
    """
    Базовое исключение для бизнес-логики API.

    Все наследники должны определять status_code и detail.
    """
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    """Пользователь с таким email уже существует (409)."""
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    """Введены неверные email или пароль (401)."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    """Токен пользователя истёк (401)."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    """Отсутствует токен в запросе (401)."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    """Неверный формат токена (401)."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    """Пользователь не найден в системе (401)."""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class RoomFullyBooked(BookingException):
    """Нет свободных номеров для бронирования (409)."""
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class RoomCannotBeBookedException(BookingException):
    """Не удалось забронировать номер по неизвестной причине (500)."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class DateFromCannotBeAfterDateTo(BookingException):
    """Дата заезда позже даты выезда (400)."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BookingException):
    """Попытка забронировать отель на срок более месяца (400)."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotAddDataToDatabase(BookingException):
    """Ошибка при добавлении данных в БД (500)."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotProcessCSV(BookingException):
    """Ошибка обработки CSV-файла (500)."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"

