"""
Celery-задачи для асинхронной обработки (учебный модуль).
-----------------------------------------------------------------
⚠️ Внимание! Модуль и весь пакет app/tasks использовались только для учебных целей.
В демонстрационной версии приложения задачи Celery не запускаются и email не рассылается.
-----------------------------------------------------------------

Реализовано:
- Ресайз изображений для папки static/images
- Email-подтверждение бронирования (только для теста, email_to_mock)
"""

import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery_app
from app.tasks.email_templates import create_booking_confirmation_template

@celery_app.task
def process_pic(path: str) -> None:
    """
    Ресайзит изображение по заданному пути и сохраняет уменьшенные копии.

    :param path: Путь к исходному изображению
    :return: None

    Ожидается, что файл лежит в файловой системе.
    Сохраняет копии в static/images с префиксами размеров.
    Логирует ошибки, если файл битый/отсутствует.
    """
    try:
        im_path = Path(path)
        im = Image.open(im_path)
        im_resized_1000_500 = im.resize((1000, 500))
        im_resized_200_100 = im.resize((200, 100))
        im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
        im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")
        print(f"Изображение {im_path.name} успешно обработано.")
    except Exception as e:
        print(f"Ошибка ресайза изображения {path}: {e}")

@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
) -> None:
    """
    Отправляет email-подтверждение бронирования (учебный пример, НЕ production!).

    :param booking: dict с данными брони ('date_from', 'date_to', опционально 'hotel', 'user')
    :param email_to: Email получателя (НЕ используется, письмо всегда идет на settings.SMTP_USER для теста)
    :return: None

    Для теста email отправляется только на адрес из settings.SMTP_USER (email_to_mock).
    Для реальной работы — заменить email_to_mock на email_to.

    Логирует ошибки при проблемах SMTP.
    """
    email_to_mock = settings.SMTP_USER  # Только для тестирования!
    msg_content = create_booking_confirmation_template(booking, email_to_mock)
    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
        print("Email успешно отправлен (только для теста, demo).")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
