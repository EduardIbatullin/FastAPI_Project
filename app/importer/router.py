"""
Роутер FastAPI для массового импорта данных об отелях, комнатах или бронях через загрузку CSV-файла.

Позволяет залить несколько объектов за раз — удобно для тестовой инициализации и интеграции с внешними системами.
Ожидается файл в формате CSV с разделителем ";". В случае ошибок структуры или сохранения — выдаёт кастомные исключения.

Пример запроса (через curl):
    curl -F "file=@hotels.csv" "http://localhost:8000/import/hotels" -H "Authorization: Bearer <TOKEN>"
"""

import codecs
import csv
from typing import Literal

from fastapi import APIRouter, UploadFile

from app.exceptions import CannotAddDataToDatabase, CannotProcessCSV
from app.importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format

router = APIRouter(
    prefix="/import",
    tags=["Импорт данных в БД"],
)


@router.post(
    "/{table_name}",
    status_code=201,
)
async def import_data_to_table(
    file: UploadFile,
    table_name: Literal["hotels", "rooms", "bookings"],
) -> dict:
    """
    Массовый импорт данных в одну из таблиц (hotels, rooms, bookings) через CSV-файл.

    :param file: Файл в формате CSV, обязательно с разделителем ';'. Первая строка — заголовки столбцов.
    :param table_name: Название целевой таблицы ("hotels", "rooms" или "bookings")
    :return: dict с ключами "result" (список добавленных объектов) и "error" (если была ошибка)

    Формат CSV (пример для hotels):
        name;location;services;rooms_quantity;image_id
        Sample Hotel;Москва;"[\"Wi-Fi\", \"Парковка\"]";10;1

    Ошибки:
        - Если файл не распознан или пуст — CannotProcessCSV (422)
        - Если не удалось добавить данные — CannotAddDataToDatabase (500)
    """
    ModelDAO = TABLE_MODEL_MAP[table_name]
    # Чтение CSV с разделителем ";"
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=";")
    data = convert_csv_to_postgres_format(csvReader)
    file.file.close()
    if not data:
        raise CannotProcessCSV
    added_data = await ModelDAO.add_bulk(data)
    if not added_data:
        raise CannotAddDataToDatabase
    return {"result": added_data, "error": ""}
