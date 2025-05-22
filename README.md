# 🏨 FastAPI Hotel Booking

Проект — это веб-приложение для онлайн-бронирования отелей "ПростоБронь". Построен на **FastAPI**, поддерживает полноценную работу с пользователями, отелями, комнатами и бронированиями.

---

## 📚 Содержание

* [Функциональность](#функциональность)
* [Технологии](#технологии)
* [Установка и запуск](#установка-и-запуск)
* [Работа с базой данных](#работа-с-базой-данных)
* [Миграции Alembic](#миграции-alembic)
* [Админ-панель](#админ-панель)
* [Кэширование](#кэширование)
* [Прометей и метрики](#прометей-и-метрики)
* [Примеры API и Web-интерфейса](#примеры)

---

## 🛠️ Функциональность

* Регистрация и авторизация пользователей
* Просмотр списка отелей и комнат
* Фильтрация по локации и датам
* Бронирование номеров
* Просмотр и удаление своих бронирований
* Админка на базе SQLAdmin
* Поддержка кеша через Redis
* Метрики через Prometheus

---

## 💻 Технологии

* **Backend**: FastAPI, SQLAlchemy 2.0, Alembic
* **База данных**: PostgreSQL
* **Auth**: OAuth2 + JWT
* **Админка**: SQLAdmin
* **Кэш**: Redis + fastapi-cache
* **Метрики**: prometheus-fastapi-instrumentator
* **Асинхронность**: asyncio, async SQLAlchemy
* **Логирование**: JSON logger (python-json-logger)

---

## 🚀 Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/EduardIbatullin/FastAPI_Project.git
cd FastAPI_Project
```

2. Создать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Настроить `.env`:

Создай `.env` на основе `.env.example`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hotel
DB_USER=postgres
DB_PASS=yourpassword
JWT_SECRET=supersecret
LOG_LEVEL=DEBUG
REDIS_HOST=localhost
REDIS_PORT=6379
```

5. Запустить сервер:

```bash
uvicorn app.main:app --reload --log-level debug
```

---

## 🗄️ Работа с базой данных

### Создание базы

Создай базу вручную в PostgreSQL, например:

```sql
CREATE DATABASE hotel;
```

---

## 🔁 Миграции Alembic

1. Инициализация (однократно):

```bash
alembic init migrations
```

2. Создание миграции:

```bash
alembic revision --autogenerate -m "initial"
```

3. Применение миграции:

```bash
alembic upgrade head
```

---

## 🔐 Админ-панель

Доступна по адресу:

```
http://localhost:8000/api/admin
```

> Требуется авторизация. Пользователь и пароль настраиваются в коде.

---

## ⚡ Кэширование

Используется Redis. Запусти Redis локально:

```bash
docker run -d -p 6379:6379 redis
```

> Кэш подключается автоматически при запуске.

---

## 📊 Прометей и метрики

Метрики доступны по адресу:

```
http://localhost:8000/metrics
```

Для подключения Prometheus добавь соответствующий `job` в конфиг.

---

## 🌐 Примеры

### Главная страница

```
http://localhost:8000/pages
```

### Информация об отеле

```
http://localhost:8000/pages/hotels/{hotel_id}?date_from=2025-06-01&date_to=2025-06-10
```

### Бронирование

```
http://localhost:8000/pages/booking?room_id=3&date_from=2025-06-01&date_to=2025-06-10
```

---

## 📎 Автор

Проект создан в обучающих целях.
Контакты и лицензия — по запросу.
