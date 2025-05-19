# FastAPI_Project

**FastAPI_Project** — это современное веб-приложение, разработанное с использованием FastAPI. Оно предназначено для управления бронированиями, отелями, номерами и пользователями, обеспечивая высокую производительность и масштабируемость.

## 🚀 Особенности

- **FastAPI**: высокопроизводительный веб-фреймворк для создания API с Python.
- **SQLAlchemy**: мощный ORM для взаимодействия с базой данных.
- **Pydantic**: валидация данных и управление настройками.
- **Alembic**: инструмент для управления миграциями базы данных.
- **Celery**: асинхронная обработка задач.
- **JWT**: аутентификация и авторизация пользователей.
- **Swagger UI**: автоматически генерируемая документация API.

## 📁 Структура проекта

```

FastAPI\_Project/
├── app/
│   ├── admin/
│   ├── bookings/
│   ├── hotels/
│   │   └── rooms/
│   ├── images/
│   ├── importer/
│   ├── pages/
│   ├── prometheus/
│   ├── tasks/
│   ├── templates/
│   ├── tests/
│   ├── users/
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│   └── main.py
├── requirements.txt
├── alembic.ini
├── README.md
└── LICENSE

````

## ⚙️ Установка и запуск

1. **Клонирование репозитория:**

   ```bash
   git clone https://github.com/EduardIbatullin/FastAPI_Project.git
   cd FastAPI_Project
````

2. **Создание и активация виртуального окружения:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. **Установка зависимостей:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Применение миграций базы данных:**

   ```bash
   alembic upgrade head
   ```

5. **Запуск приложения:**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Доступ к документации API:**

   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   * ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧪 Тестирование

```bash
pytest
```

Тесты расположены в директории `app/tests/` и включают как модульные, так и интеграционные тесты.

## 📦 Зависимости

* `fastapi`
* `uvicorn`
* `sqlalchemy`
* `alembic`
* `pydantic`
* `celery`
* `python-jose`
* `passlib`
* `pytest`
* `jinja2`
* `prometheus-client`
* `aiofiles`

Полный список зависимостей указан в файле `requirements.txt`.

## 📝 Лицензия

Этот проект лицензирован под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.
