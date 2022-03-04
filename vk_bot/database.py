import os
import sqlite3
from sqlite3 import Connection
from typing import Any, Optional

from vk_bot.sql_queries import Create


class BotDatabase:
    """
    Взаимодействие с базой данных.
    """

    def __init__(self):
        self.name_db = 'bot.db'

    def gen_database(self) -> Connection:
        """
        Создание базы данных, подключение к ней и генерация таблиц.

        Returns
        -------
        Connection
            Объект соединения с базой данных.
        """

        table_creation_queries = [Create.USERS, Create.EXTREMES]
        try:
            connection = sqlite3.connect(self.name_db)
            for query in table_creation_queries:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            return connection
        except sqlite3.Error as error:
            print("Ошибка при CREATE запросе:", error)

    def get_connection(self) -> Connection:
        """
        Подключение к базе данных.

        Returns
        -------
        Connection
             Объект соединения с базой данных.
        """
        listdir = os.listdir()
        if self.name_db in listdir:
            try:
                return sqlite3.connect(self.name_db)
            except sqlite3.Error as error:
                print("Ошибка при подключении к sqlite:", error)
        else:
            return self.gen_database()

    def select(self, query: str, input_value: Optional[tuple] = None) -> Any:
        """
        Исполнение SELECT-запроса к базе данных.

        Parameters
        ----------
        query : str
            SELECT-запрос в виде строки.
        input_value : tuple
            Данные в виде кортежа, которые подставляются в запрос.

        Returns
        -------
        Any
            Результат запроса к базе данных.
        """

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            if input_value:
                cursor.execute(query, input_value)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as error:
            print("Ошибка при SELECT запросе:", error)
        finally:
            if connection:
                connection.close()

    def insert(self, query: str, input_value: tuple):
        """
        Исполнение INSERT-запроса к базе данных.

        Parameters
        ----------
        query : str
            SELECT-запрос в виде строки.
        input_value : tuple
            Данные в виде кортежа, которые подставляются в запрос.
        """

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, input_value)
            connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при INSERT запросе:", error)
        finally:
            if connection:
                connection.close()

    def update(self, query: str, input_value: tuple):
        """
        Исполнение UPDATE-запроса к базе данных.

        Parameters
        ----------
        query : str
            SELECT-запрос в виде строки.
        input_value : tuple
            Данные в виде кортежа, которые подставляются в запрос.
        """

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, input_value)
            connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при UPDATE запросе", error)
        finally:
            if connection:
                connection.close()
