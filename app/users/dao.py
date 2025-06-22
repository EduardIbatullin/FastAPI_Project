"""
DAO для пользователей.
Наследует стандартные CRUD-операции из BaseDAO:
- find_one_or_none, find_by_id, find_all, add, delete и др.
Используйте UsersDAO для поиска, добавления, удаления пользователей в базе.
"""

from app.dao.base import BaseDAO
from app.users.models import Users

class UsersDAO(BaseDAO):
    """
    Data Access Object для таблицы users.
    Использует model=Users. Пример:
        user = await UsersDAO.find_one_or_none(email="mail@example.com")
    """
    model = Users
