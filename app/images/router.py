"""
Роутер FastAPI для загрузки изображений для отелей/номеров.

Загруженный файл сохраняется как app/static/images/{name}.webp и обрабатывается асинхронно.
Пример использования:
    POST /images/hotels?name=5 с файлом — сохранит картинку как 5.webp.

ВНИМАНИЕ: Это демонстрационная реализация. В production путь к картинкам и обработка должны настраиваться через config.
"""

import shutil

from fastapi import APIRouter, UploadFile
from fastapi_versioning import version

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"],
)


@router.post("/hotels")
@version(1)
async def add_hotel_image(name: int, file: UploadFile) -> None:
    """
    Загрузить изображение для отеля/номера.

    :param name: числовой идентификатор (например, 1 — будет app/static/images/1.webp)
    :param file: файл изображения (ожидается, что это .webp, .png, .jpg — ограничений нет)
    :return: None (если успешно)

    После сохранения файла происходит асинхронная обработка (process_pic.delay).
    Файлы сохраняются в app/static/images/, имя — по шаблону {name}.webp.

    Пример:
        curl -F "file=@hotel1.webp" "http://localhost:8000/images/hotels?name=1"
    """
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    # Асинхронная post-обработка файла (например, ресайз, конвертация)
    process_pic.delay(im_path)
