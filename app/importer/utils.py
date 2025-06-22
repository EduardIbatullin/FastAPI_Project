"""
Утилиты для импорта данных из CSV в БД.

- TABLE_MODEL_MAP: маппинг названия таблицы (hotels, rooms, bookings) на соответствующий DAO-класс.
- convert_csv_to_postgres_format: функция преобразования строк из CSV к формату, пригодному для записи в БД.
"""

from datetime import datetime
import json
from typing import Iterable

from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.logger import logger

# Пример использования:
#   ModelDAO = TABLE_MODEL_MAP["hotels"]
#   data = convert_csv_to_postgres_format(csv.DictReader(...))
#   ModelDAO.add_bulk(data)

TABLE_MODEL_MAP = {
    "hotels": HotelDAO,
    "rooms": RoomDAO,
    "bookings": BookingDAO,
}

def convert_csv_to_postgres_format(csv_iterable: Iterable) -> list[dict]:
    """
    Преобразует строки из CSV в формат, пригодный для PostgreSQL и ORM-DAO.

    Ожидаемый формат CSV:
        - Числовые поля (id, quantity, price, image_id и др.) хранятся как строки, преобразуются в int.
        - Поле services (строка) содержит JSON-список услуг, например: ["Wi-Fi", "Парковка"]
        - Поля с 'date' преобразуются к datetime (YYYY-MM-DD)
        - Пустые значения остаются пустыми.

    :param csv_iterable: iterable (например, csv.DictReader), где каждая строка — dict с полями CSV.
    :return: список dict, пригодных для записи в БД.
    :raises: В случае ошибки возвращает пустой список и логгирует ошибку.

    Пример строки на входе:
        {
            "name": "Sample Hotel",
            "location": "Москва",
            "services": "[\"Wi-Fi\", \"Парковка\"]",
            "rooms_quantity": "10",
            "image_id": "1"
        }
    """
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v is None or v == "":
                    continue
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    try:
                        row[k] = json.loads(v.replace("'", '"'))
                    except Exception:
                        logger.error(f"Не удалось декодировать поле services: {v!r}")
                        row[k] = []
                elif "date" in k:
                    try:
                        row[k] = datetime.strptime(v, "%Y-%m-%d")
                    except Exception:
                        logger.error(f"Некорректная дата: {k}={v!r}")
                        row[k] = None
            data.append(row)
        return data
    except Exception:
        logger.error("Cannot convert CSV into DB format", exc_info=True)
        return []
