"""
Роутер для тестирования мониторинга Grafana и Prometheus.
-----------------------------------------------------------------
⚠️ Внимание! Все endpoints в этом файле предназначены только для учебных целей и тестирования мониторинга.
В демонстрационной и production-версии приложения данные endpoints не используются!
-----------------------------------------------------------------

Содержит endpoints для генерации ошибок, задержек и искусственной нагрузки.
"""

import time
from random import random

from fastapi import APIRouter

router = APIRouter(
    prefix="/prometheus",
    tags=["Тестирование Grafana + Prometheus (учебное)"]
)

@router.get("/get_error")
def get_error() -> None:
    """
    Выбрасывает случайную ошибку (ZeroDivisionError или KeyError).

    Используется для тестирования alert-правил в Grafana/Prometheus.
    Не имеет бизнес-смысла, не использовать в продакшене!
    """
    if random() > 0.5:
        raise ZeroDivisionError("Деление на ноль (симулировано для мониторинга)")
    else:
        raise KeyError("Ключ не найден (симулировано для мониторинга)")

@router.get("/time_consumer")
def time_consumer() -> int:
    """
    Задерживает ответ на случайное время до 5 секунд.

    Используется для симуляции "медленных" запросов и сбора latency-метрик.
    Не использовать в боевом приложении.
    :return: всегда 1
    """
    delay = random() * 5
    time.sleep(delay)
    return 1

@router.get("/memory_consumer")
def memory_consumer() -> int:
    """
    Потребляет большое количество оперативной памяти (создаёт большой список).

    Используется для теста метрик и алёртов по памяти.
    Не использовать в реальных сценариях!
    :return: всегда 1
    """
    _ = [i for i in range(30_000_000)]  # >200 МБ памяти
    return 1
