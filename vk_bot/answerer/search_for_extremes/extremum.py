from vk_bot.database import BotDatabase
from vk_bot.sql_queries import Select, Insert, Update


class Extremum:
    def __init__(self, db: BotDatabase, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_step(self) -> str:
        """
        Извлечение шага, на котором находится пользователь при решении задачи.

        Returns
        -------
        str
            Шаг, на котором находится пользователь, для решения задачи.
        """

        if not self.db.select(Select.EXTREMES_STEP, (self.user_id,)):
            self.registration()
        return self.db.select(Select.EXTREMES_STEP, (self.user_id,))[0]

    def get_type(self):
        return self.db.select(Select.EXTREMES_TYPE, (self.user_id,))[0]

    def get_restr(self):
        return self.db.select(Select.EXTREMES_RESTR, (self.user_id,))[0]

    def get_vars(self):
        return self.db.select(Select.EXTREMES_VARS, (self.user_id,))[0]

    def get_params(self, task_type, interval):
        if task_type == 'common':
            if interval == 'with_int':
                return self.db.select(Select.EXTREMES_WITH_INT, (self.user_id,))
            else:
                print(self.db.select(Select.EXTREMES_WITHOUT_INT, (self.user_id,)))
                return self.db.select(Select.EXTREMES_WITHOUT_INT, (self.user_id,))
        else:
            if interval == 'with_int':
                return self.db.select(Select.EXTREMES_RESTR_WITH_INT, (self.user_id,))
            else:
                return self.db.select(Select.EXTREMES_RESTR_WITHOUT_INT, (self.user_id,))

    def update_step(self, step: str):
        self.db.update(Update.EXTREMES_STEP, (step, self.user_id))

    def update_type(self, task_type: str):
        self.db.update(Update.EXTREMES_TYPE, (task_type, self.user_id))

    def update_restr(self, restr: bool):
        if restr:
            self.db.update(Update.EXTREMES_RESTR, (1, self.user_id))
        else:
            self.db.update(Update.EXTREMES_RESTR, (0, self.user_id))

    def update_vars(self, vars):
        self.db.update(Update.EXTREMES_VARS, (vars, self.user_id))

    def update_func(self, func):
        self.db.update(Update.EXTREMES_FUNC, (func, self.user_id))

    def update_g_func(self, g_func):
        self.db.update(Update.EXTREMES_G_FUNC, (g_func, self.user_id))

    def update_interval_x(self, interval_x):
        self.db.update(Update.EXTREMES_INTERVAL_X, (interval_x, self.user_id))

    def update_interval_y(self, interval_y):
        self.db.update(Update.EXTREMES_INTERVAL_Y, (interval_y, self.user_id))

    def registration(self):
        """
        Регистрация пользователя в базе данных в таблице extremum.
        """

        self.db.insert(Insert.EXTREMES, (self.user_id,))



