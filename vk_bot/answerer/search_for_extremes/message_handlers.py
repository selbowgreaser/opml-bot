from vk_api.vk_api import VkApiMethod

from solver_core.search_for_extremes.handlers.input_validation import check_variables, check_restr_func, \
    check_expression, check_limits
from solver_core.search_for_extremes.handlers.preprocessing import prepare_data
from solver_core.search_for_extremes.local_extr import LocalExtr
from vk_bot.answerer.response_init import Response
from vk_bot.answerer.search_for_extremes.extremum import Extremum
from vk_bot.answerer.search_for_extremes.keyboards import Keyboards
from vk_bot.answerer.search_for_extremes.scripted_phrases import Phrases
from vk_bot.database import BotDatabase
from vk_bot.user import User


class Handlers:
    """
    Генератор ответов пользователю.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект соединения с VK и набор методов API.
    db : BotDatabase
        Объект для взаимодействия с базой данных.
    user : User
        Объект для взаимодействия с данными пользователя.
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User, extremum: Extremum):
        self.vk = vk_api_method
        self.db = db
        self.user = user
        self.extremum = extremum
        self.response = Response(self.user.user_id)

    def task_type_selection(self) -> Response:
        """
        Выбор типа задачи.
        Шаг: task_type_selection

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.extremum.update_step('task_type_selection')
        self.response.set_text(Phrases.TASK_TYPE_SELECTION)
        self.response.set_keyboard(Keyboards().for_task_type_selection())
        return self.response

    def input_vars(self) -> Response:
        """
        Предложение ввести имена переменных.
        Шаг: input_vars

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.extremum.update_step('input_vars')
        self.response.set_text(Phrases.INPUT_VARS)
        return self.response

    def vars(self, text) -> Response:
        """
        Обработка введенных именных переменных. Предложение ввести функцию.
        Шаг: input_func

        Parameters
        ----------
        text : str
            Текст сообщения, отправленного пользователем.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        try:
            vars = check_variables(text)
            self.extremum.update_vars(vars)
            self.response.set_text(Phrases.INPUT_FUNC)
            self.extremum.update_step('input_func')
            return self.response
        except ValueError as e:
            return self.error(e)

    def func(self, text, task_type) -> Response:
        try:
            vars = self.extremum.get_vars()
            func = check_expression(text, vars)
            self.extremum.update_func(func)
            if task_type == 'common':
                self.response.set_text(Phrases.INPUT_RESTR)
                self.response.set_keyboard(Keyboards().for_input_restr())
                self.extremum.update_step('input_restr')
            else:
                self.response.set_text(Phrases.INPUT_G_FUNC)
                self.extremum.update_step('input_g_func')
            return self.response
        except ValueError as e:
            return self.error(e)

    def g_func(self, text) -> Response:
        try:
            vars = self.extremum.get_vars()
            g_func = check_restr_func(text, vars)
            self.extremum.update_g_func(g_func)
            self.extremum.update_step('input_restr')
            self.response.set_text(Phrases.INPUT_RESTR)
            self.response.set_keyboard(Keyboards().for_input_restr())
            return self.response
        except ValueError as e:
            return self.error(e)

    def input_restr(self) -> Response:
        self.extremum.update_step('input_interval_x')
        self.response.set_text(Phrases.INPUT_INTERVAL_X)
        return self.response

    def interval_x(self, text) -> Response:
        try:
            interval_x = check_limits(text)
            self.extremum.update_interval_x(interval_x)
            self.extremum.update_step('input_interval_y')
            self.response.set_text(Phrases.INPUT_INTERVAL_Y)
            return self.response
        except ValueError as e:
            return self.error(e)

    def interval_y(self, text) -> Response:
        try:
            interval_y = check_limits(text)
            self.extremum.update_interval_y(interval_y)
            self.extremum.update_step('compute')
            self.response.set_text(Phrases.COMPUTE)
            self.response.set_keyboard(Keyboards().for_compute())
            return self.response
        except ValueError as e:
            return self.error(e)

    def precompute(self) -> Response:
        self.extremum.update_step('compute')
        self.response.set_text(Phrases.COMPUTE)
        self.response.set_keyboard(Keyboards().for_compute())
        return self.response

    def local_extr(self, restr) -> Response:
        if restr:
            vars, func, interval_x, interval_y = self.extremum.get_params(self.extremum.get_type(), 'with_int')
            param = prepare_data(vars=vars, func=func, interval_x=interval_x, interval_y=interval_y)
        else:
            vars, func = self.extremum.get_params(self.extremum.get_type(), 'without_int')
            param = prepare_data(vars=vars, func=func)
        solver = LocalExtr(**param)
        result = solver.solve()
        link = '\n\nСЮДА НАДО ДОБАВИТЬ ССЫЛКУ'
        self.response.set_text(result+link)
        self.response.set_keyboard(Keyboards().for_menu())
        self.extremum.update_step('start')
        self.user.update_status('menu')
        return self.response

    def local_extr_with_restr(self, restr) -> Response:
        if restr:
            vars, func, g_func, interval_x, interval_y = self.extremum.get_params(self.extremum.get_type(), 'with_int')
            param = prepare_data(vars=vars, func=func, interval_x=interval_x, interval_y=interval_y)
        else:
            vars, func, g_func = self.extremum.get_params(self.extremum.get_type(), 'without_int')
            param = prepare_data(vars=vars, func=func)
        solver = LocalExtr(**param)
        result = solver.solve()
        link = '\n\nСЮДА НАДО ДОБАВИТЬ ССЫЛКУ'
        self.response.set_text(result + link)
        self.response.set_keyboard(Keyboards().for_menu())
        self.extremum.update_step('start')
        self.user.update_status('menu')
        return self.response

    def click_button(self) -> Response:
        """
        Если пользователь ввёл непонятное сообщение.
        Статус: не переопределяется

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        self.response.set_text(Phrases.CLICK_BUTTON)
        return self.response

    def error(self, error) -> Response:
        self.response.set_text(Phrases.ERROR.format(error))
        return self.response
