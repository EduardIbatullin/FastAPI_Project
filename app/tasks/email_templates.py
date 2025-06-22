"""
Email-шаблоны для отправки пользователям (только учебный пример).
-----------------------------------------------------------------
⚠️ Модуль и весь пакет app/tasks использовались только для учебных целей!
В демонстрационной версии приложения отправка email не используется.
-----------------------------------------------------------------

Реализовано: подтверждение бронирования.
Можно расширять для других сценариев (plain text, вложения и т.д.).
"""

from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings

def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
) -> EmailMessage:
    """
    Формирует email-сообщение подтверждения бронирования.

    :param booking: словарь с ключами 'date_from', 'date_to', (опционально: 'hotel', 'user')
    :param email_to: Email получателя
    :return: EmailMessage с html-письмом

    Требуемая структура booking:
        {
            "date_from": str (YYYY-MM-DD),
            "date_to": str (YYYY-MM-DD),
            "hotel": str (опционально),
            "user": str (опционально)
        }
    """
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    # Формируем HTML-тело письма. Добавляем hotel и user если есть.
    hotel_name = booking.get("hotel", "")
    user_name = booking.get("user", "")
    date_from = booking.get("date_from", "?")
    date_to = booking.get("date_to", "?")

    html_content = f"""
        <h1>Подтверждение бронирования</h1>
        <p>Здравствуйте{', ' + user_name if user_name else ''}!</p>
        <p>
            Ваше бронирование
            {f"отеля <b>{hotel_name}</b>" if hotel_name else "номера"}
            c <b>{date_from}</b> по <b>{date_to}</b> подтверждено.
        </p>
        <p>Спасибо за выбор нашего сервиса!</p>
    """

    email.set_content(html_content, subtype="html")
    return email
