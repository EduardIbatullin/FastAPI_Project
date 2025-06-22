"""
Конфигурация Celery для асинхронных задач (учебный пример).
----------------------------------------------------------------------
⚠️ Модуль и весь пакет app/tasks использовались только в учебном процессе!
В демонстрационной версии приложения асинхронные задачи не запускаются
и celery worker не требуется.
----------------------------------------------------------------------

- Использует Redis как брокер сообщений.
- Все задачи описаны в app.tasks.tasks.
- Для реального запуска worker нужно отдельной командой:
    celery -A app.tasks.celery_app.celery_app worker --loglevel=info

Переменные окружения:
    REDIS_HOST, REDIS_PORT — используются для подключения к брокеру.
"""

from celery import Celery
from app.config import settings

# Создаём Celery app с брокером Redis
celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]  # все задачи лежат в tasks.py
)

# Включаем автоподключение к брокеру при рестарте (актуально для docker-compose/CI)
celery_app.conf.update(
    broker_connection_retry_on_startup=True
)
