import os
import sqlite3


class BotDatabase:
    def __init__(self):
        self.name_db = 'users.db'

    def gen_database(self):
        table_creation_queries = ["CREATE TABLE users ("
                                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                  "user_id INTEGER NOT NULL, "
                                  "first_name TEXT NOT NULL, "
                                  "last_name TEXT NOT NULL, "
                                  "status TEXT DEFAULT 'welcome')",
                                  "CREATE TABLE data ("
                                  "user_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                  "vars TEXT, "
                                  "func TEXT, "
                                  "interval_x TEXT, "
                                  "interval_y TEXT, "
                                  "g_func TEXT, "
                                  "restr TEXT, "
                                  "FOREIGN KEY(user_id) REFERENCES users(id))"
                                  ]
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

    def insert_query(self, data):
        query = "INSERT INTO users(user_id, first_name, last_name) VALUES (?, ?, ?)"
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

    def update_query(self, data):
        query = "UPDATE users SET status = ? WHERE user_id = ?"
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
