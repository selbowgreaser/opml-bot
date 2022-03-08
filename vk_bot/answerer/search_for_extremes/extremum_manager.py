from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.response_init import Response
from vk_bot.answerer.search_for_extremes.extremum import Extremum
from vk_bot.answerer.search_for_extremes.message_handlers import Handlers
from vk_bot.database import BotDatabase
from vk_bot.user import User


class ExtremumManager:
    """
    Менеджер управления решением задачи поиска экстремума.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект соединения с VK и набор методов API.
    db : BotDatabase
        Объект для взаимодействия с базой данных.
    user : User
        Объект для взаимодействия с данными пользователя.
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User):
        self.vk_api_method = vk_api_method
        self.db = db
        self.user = user
        self.extremum = Extremum(db, user.user_id)
        self.step = self.extremum.get_step()
        self.type = self.extremum.get_type()
        self.restr = self.extremum.get_restr()
        self.handlers = Handlers(vk_api_method, db, user, self.extremum)

    def manage(self, text: str) -> Response:
        """
        Управление обработкой входящих сообщений для ввода исходных данных в задаче.

        Parameters
        ----------
        text : str
            Текст сообщения, отправленного пользователем.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        if self.step == 'start':
            return self.handlers.task_type_selection()

        if self.step == 'task_type_selection':
            if text == 'Обычная':
                self.extremum.update_type('common')
            elif text == 'С ограничивающей функцией':
                self.extremum.update_type('with_lim_func')
            else:
                return self.handlers.click_button()
            return self.handlers.input_vars()

        if self.step == 'input_vars':
            return self.handlers.vars(text)

        if self.step == 'input_func':
            return self.handlers.func(text, self.type)

        if self.step == 'input_g_func':
            return self.handlers.g_func(text)

        if self.step == 'input_restr':
            if text == 'Да':
                self.extremum.update_restr(True)
                return self.handlers.input_restr()
            elif text == 'Нет':
                self.extremum.update_restr(False)
                return self.handlers.precompute()
            else:
                return self.handlers.click_button()

        if self.step == 'input_interval_x':
            return self.handlers.interval_x(text)

        if self.step == 'input_interval_y':
            return self.handlers.interval_y(text)

        if self.step == 'compute':
            if self.type == 'common':
                return self.handlers.local_extr(self.restr)
            else:
                return self.handlers.local_extr_with_restr(self.restr)
