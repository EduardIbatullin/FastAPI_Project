"""
Базовый DAO-класс для асинхронного доступа к базе данных через SQLAlchemy.

- Реализует универсальные CRUD-методы: поиск, добавление, удаление записей.
- Используется только как родительский класс — в наследнике обязательно определить атрибут model!
- Все операции выполняются через async-сессии.
- Осторожно: массовые add/delete без фильтра могут привести к ошибкам или потере данных.
"""

from sqlalchemy import delete, insert, select

from app.database import async_session_maker


class BaseDAO:
    """
    Базовый Data Access Object.

    Атрибуты:
        model: SQLAlchemy-модель, с которой работает конкретный DAO.
            ВНИМАНИЕ: всегда переопределяйте model в наследнике!
    """
    model = None  # Должен быть определён в наследуемом классе (например: model = Bookings)

    @classmethod
    async def find_by_id(cls, model_id: int) -> dict | None:
        """
        Возвращает одну запись по id как dict, либо None, если не найдено.

        :param model_id: ID записи
        :return: dict (ключи как в модели) или None
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> dict | None:
        """
        Возвращает одну запись по фильтру как dict, либо None.

        :param filter_by: критерии фильтрации (name=value)
        :return: dict или None
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> list[dict]:
        """
        Возвращает все записи по фильтру как список dict.

        :param filter_by: критерии фильтрации (name=value)
        :return: list[dict]
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data) -> None:
        """
        Добавляет запись в базу данных.
        ВНИМАНИЕ: Возвращает None! Для получения id новой записи — расширьте метод в наследнике.

        :param data: параметры для вставки (name=value)
        """
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by) -> None:
        """
        Удаляет записи по фильтру.
        ОПАСНО: при отсутствии фильтра удалит все записи таблицы!

        :param filter_by: критерии фильтрации (name=value)
        """
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
