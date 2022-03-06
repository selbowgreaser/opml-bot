from typing import NamedTuple


class Create(NamedTuple):
    """
    Запросы на создание таблиц в базе данных.
    """
    USERS = ("CREATE TABLE users (\n"
             "               user_id INTEGER PRIMARY KEY, \n"
             "               first_name TEXT NOT NULL, \n"
             "               last_name TEXT NOT NULL, \n"
             "               status TEXT DEFAULT 'start')")

    EXTREMES = ("CREATE TABLE extremes (\n"
                "                  user_id INTEGER PRIMARY KEY, \n"
                "                  step TEXT DEFAULT 'start',\n"
                "                  type INTEGER DEFAULT 0,\n"
                "                  vars TEXT, \n"
                "                  func TEXT, \n"
                "                  interval_x TEXT, \n"
                "                  interval_y TEXT, \n"
                "                  g_func TEXT, \n"
                "                  restr INTEGER, \n"
                "                  FOREIGN KEY(user_id) REFERENCES users(user_id))")


class Insert(NamedTuple):
    """
    Запросы на добавление новых строк в таблицу базы данных.
    """

    USERS = "INSERT INTO users(user_id, first_name, last_name) VALUES (?, ?, ?)"
    EXTREMES = "INSERT INTO extremes(user_id) VALUES (?)"


class Select(NamedTuple):
    """
    Запросы на извлечение полей из таблицы базы данных.
    """

    USERS_USER_ID = "SELECT user_id FROM users WHERE user_id = ?"
    USERS_STATUS = "SELECT status FROM users WHERE user_id = ?"

    EXTREMES_STEP = "SELECT step FROM extremes WHERE user_id = ?"
    EXTREMES_VARS = "SELECT vars FROM extremes WHERE user_id = ?"
    EXTREMES_TYPE = "SELECT type FROM extremes WHERE user_id = ?"
    EXTREMES_ALL = "SELECT vars, func, g_func, restr, interval_x, interval_y FROM extremes WHERE user_id = ?"


class Update(NamedTuple):
    """
    Запросы на обновление полей в таблицах базы данных.
    """

    USERS_STATUS = "UPDATE users SET status = ? WHERE user_id = ?"

    EXTREMES_STEP = "UPDATE extremes SET step = ? WHERE user_id = ?"
    EXTREMES_TYPE = "UPDATE extremes SET type = ? WHERE user_id = ?"
    EXTREMES_VARS = "UPDATE extremes SET vars = ? WHERE user_id = ?"
    EXTREMES_FUNC = "UPDATE extremes SET func = ? WHERE user_id = ?"
    EXTREMES_G_FUNC = "UPDATE extremes SET g_func = ? WHERE user_id = ?"
    EXTREMES_RESTR = "UPDATE extremes SET restr = ? WHERE user_id = ?"
    EXTREMES_INTERVAL_X = "UPDATE extremes SET interval_x = ? WHERE user_id = ?"
    EXTREMES_INTERVAL_Y = "UPDATE extremes SET interval_y = ? WHERE user_id = ?"

