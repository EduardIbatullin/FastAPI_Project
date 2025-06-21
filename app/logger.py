"""
Глобальная настройка логгирования проекта.

- Все логи форматируются в JSON через pythonjsonlogger.
- Формат лога: timestamp (UTC), level, message, module, funcName.
- Логгер и уровень логирования управляются через переменные из .env.
- Модуль импортируется как `from app.logger import logger` и используется по всему проекту.
"""

import logging
import os
from datetime import datetime
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

# Загружает переменные окружения из файла .env (например, LOG_LEVEL)
load_dotenv()

logger = logging.getLogger()
log_handler = logging.StreamHandler()

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Форматирует логи в JSON с ключами:
    - timestamp: время события (UTC, формат ISO)
    - level: уровень лога (INFO, WARNING, ERROR, etc.)
    - message: текст сообщения
    - module: модуль, из которого пришёл лог
    - funcName: функция, откуда вызван лог

    Использование UTC времени гарантирует единый таймстемп вне зависимости от сервера.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Уровень логирования можно задать через .env (например, LOG_LEVEL=DEBUG)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)
