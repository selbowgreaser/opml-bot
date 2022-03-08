from typing import Optional

from vk_api.vk_api import VkApiMethod

from vk_bot.sql_queries import Select, Insert, Update
from database import BotDatabase


class User:
    """
    Дает возможность взаимодействовать с информацией о пользователе в базе данных: регистрировать, авторизовываться,
    обновлять данные. Получение информации о пользователе с помощью API-методов.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект для обращений к методам API VK.
    db: BotDatabase
        Объект для работы с базой данных.
    user_id: int
        id пользователя, от которого пришло сообщение
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user_id: int):
        self.vk_api_method = vk_api_method
        self.db = db
        self.user_id = user_id

    def authorization(self) -> str:
        """
        Авторизация пользователя (извлечение статуса из базы данных) и регистрация, когда информация о пользователе
        отсутствует в базе данных.

        Returns
        -------
        str
            Статус пользователя в общении с ботом.
        """

        if not self.db.select(Select.USERS_USER_ID, (self.user_id,)):
            self.registration()
        return self.db.select(Select.USERS_STATUS, (self.user_id,))[0]

    def registration(self):
        """
        Регистрация пользователя в базе данных в таблице users.
        """

        self.db.insert(Insert.USERS, (self.user_id, self.get_first_name(), self.get_last_name()))

    def update_status(self, status: str):
        """
        Обновление статус пользователя в базе данных.

        Parameters
        ----------
        status : str
            Статус пользователя в общении с ботом.
        """

        self.db.update(Update.USERS_STATUS, (status, self.user_id))

    def get_first_name(self) -> str:
        """
        Получение имени пользователя с помощью API VK.

        Returns
        -------
        str
            Имя пользователя.
        """

        return self.vk_api_method.users.get(user_id=self.user_id)[0]['first_name']

    def get_last_name(self) -> str:
        """
        Получение фамилии пользователя с помощью API VK.

        Returns
        -------
        str
            Фамилия пользователя.
        """

        return self.vk_api_method.users.get(user_id=self.user_id)[0]['last_name']

