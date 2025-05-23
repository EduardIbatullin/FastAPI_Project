import logging
import os
from datetime import datetime
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

load_dotenv()  # <-- ДОСТАЁТ ПЕРЕМЕННЫЕ ИЗ .env

logger = logging.getLogger()
logHandler = logging.StreamHandler()

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
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
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)
