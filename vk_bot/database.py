import os
import sqlite3

from vk_bot.sql_queries import CREATE_USERS, CREATE_DATA, INSERT_USERS, INSERT_DATA, UPDATE_USERS, UPDATE_DATA


class BotDatabase:
    def __init__(self):
        self.name_db = 'bot.db'

    def gen_database(self):
        table_creation_queries = [CREATE_USERS, CREATE_DATA]
        try:
            connection = sqlite3.connect(self.name_db)
            for query in table_creation_queries:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            return connection
        except sqlite3.Error as error:
            print("Ошибка при CREATE запросе", error)

    def get_connection(self):
        listdir = os.listdir()
        if self.name_db in listdir:
            try:
                return sqlite3.connect(self.name_db)
            except sqlite3.Error as error:
                print("Ошибка при подключении к sqlite", error)
        else:
            return self.gen_database()

    def select_query(self, query, input_value=None):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            if input_value:
                cursor.execute(query, input_value)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as error:
            print("Ошибка при SELECT запросе", error)
        finally:
            if connection:
                connection.close()

    def insert_query(self, table, data):
        if table == 'users':
            query = INSERT_USERS
        elif table == 'data':
            query = INSERT_DATA
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при INSERT запросе", error)
        finally:
            if connection:
                connection.close()

    def update_query(self, data, column=None, table='users'):
        if table == 'users':
            query = UPDATE_USERS
        else:
            query = UPDATE_DATA.format(column)
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при UPDATE запросе", error)
        finally:
            if connection:
                connection.close()
