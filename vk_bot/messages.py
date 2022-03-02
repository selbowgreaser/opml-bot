from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import handler_input_data.handler
from LocalExtr import LocalExtr
from LocalExtrWithRestrictions import LocalExtrWithRestrictions
from user import User
from vk_bot.database import BotDatabase
from vk_bot.sql_queries import SELECT_DATA


class Handler:
    def __init__(self, vk, user_id, message):
        self.vk = vk
        self.user = User(user_id)
        self.user_id = user_id
        self.message = message
        self.name, self.status = self.user.authorization()
        self.task = BotDatabase().select_query(SELECT_DATA.format('task'), (self.user_id,))[0]

    def set_message(self, answer, keyboard=None):
        answer = answer
        keyboard = keyboard
        self.vk.send_message(self.user_id, answer, keyboard)

    def story(self):
        if self.status == 'welcome':
            if self.message == 'МЕНЮ':
                return self.handler_menu()
            return self.handler_welcome()

        if self.status == 'menu':
            if self.message == "1":
                return self.handler_local_extr()
            elif self.message == "2":
                return self.handler_local_extr_with_rest()
            return self.handler_menu()

        if self.status == '1':
            return self.handler_vars()

        if self.status == '2':
            return self.handler_vars()

        if self.status == 'vars':
            return self.handler_func()

        if self.status == 'func':
            if self.task == 1:
                if self.message == 'Да':
                    BotDatabase().update_query((1, self.user_id), column='restr', table='data')
                    self.user.update_status('func')
                    return self.handler_restr()
                elif self.message == 'Нет':
                    BotDatabase().update_query((0, self.user_id), column='restr', table='data')
                    return self.handler_local_extr_res()
                return self.handler_error('')
            else:
                return self.handler_g_func()

        if self.status == 'g_func':
            if self.message == 'Да':
                BotDatabase().update_query((1, self.user_id), column='restr', table='data')
                self.user.update_status('func')
                return self.handler_restr()
            elif self.message == 'Нет':
                BotDatabase().update_query((0, self.user_id), column='restr', table='data')
                return self.handler_local_extr_with_rest_res()
            return self.handler_error('')

        if self.status == 'interval_x':
            return self.handler_interval_x()

        if self.status == 'interval_y':
            return self.handler_interval_y()

    def handler_welcome(self):
        answer = f"Привет, {self.name}!\n\nНажми на кнопочку!"
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("МЕНЮ", color=VkKeyboardColor.POSITIVE)
        self.set_message(answer, keyboard.get_keyboard())

    def handler_menu(self):
        self.user.update_status('menu')
        answer = f"Возможности бота:\n\n" \
                 f"1. Найти локальный экстремум функции двух переменных\n" \
                 f"2. Найти локальный экстремум функции двух переменных с ограничениями (методом Лагранжа)"
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("1", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("2", color=VkKeyboardColor.POSITIVE)
        self.set_message(answer, keyboard.get_keyboard())

    def handler_local_extr(self):
        self.user.update_status('1')
        BotDatabase().update_query((1, self.user_id), column='task', table='data')
        answer = "Следующими несколькими сообщениями тебе нужно будет ввести необходимые данные.\n\n"
        answer += "Введи имена переменных через пробел.\n\nНапример:\nx1 x2"
        self.set_message(answer)

    def handler_local_extr_with_rest(self):
        self.user.update_status('2')
        BotDatabase().update_query((2, self.user_id), column='task', table='data')
        answer = "Следующими несколькими сообщениями тебе нужно будет ввести необходимые данные.\n\n"
        answer += "Введи имена переменных через пробел.\n\nНапример:\nx1 x2"
        self.set_message(answer)

    def handler_vars(self):
        try:
            vars = handler_input_data.handler.check_variables(self.message)
            self.user.update_status('vars')
            BotDatabase().update_query((vars, self.user_id), column='vars', table='data')
            answer = "Всё окей!\n\n"
            answer += "Теперь введи функцию.\n\nНапример:\nx1**2 + 0.5*x2**2"
            self.set_message(answer)
        except ValueError as error:
            self.handler_error(error)

    def handler_func(self):
        try:
            vars = BotDatabase().select_query(SELECT_DATA.format('vars'), (self.user_id, ))[0].split()
            func = handler_input_data.handler.check_expression(self.message, vars)
            self.user.update_status('func')
            BotDatabase().update_query((func, self.user_id), column='func', table='data')
            answer = "Хорошо!\n\n"
            if self.task == 1:
                answer += "Есть ли у твоей функции ограничения?"
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Да", color=VkKeyboardColor.POSITIVE)
                keyboard.add_button("Нет", color=VkKeyboardColor.NEGATIVE)
                self.set_message(answer, keyboard.get_keyboard())
            else:
                answer += "Введи ограничивающую функцию.\n\nНапример:\nx1**3+x2**3-1"
                self.set_message(answer)
        except (ValueError, SyntaxError, NameError) as error:
            self.handler_error(error)

    def handler_g_func(self):
        try:
            vars = BotDatabase().select_query(SELECT_DATA.format('vars'), (self.user_id,))[0].split()
            g_func = handler_input_data.handler.check_restr_func(self.message, vars)
            self.user.update_status('g_func')
            BotDatabase().update_query((g_func, self.user_id), column='g_func', table='data')
            answer = "Хорошо!\n\n"
            answer += "Есть ли у твоей функции ограничения?"
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Да", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Нет", color=VkKeyboardColor.NEGATIVE)
            self.set_message(answer, keyboard.get_keyboard())
        except (ValueError, SyntaxError) as error:
            self.handler_error(error)

    def handler_restr(self):
        answer = 'Введи ограничения по оси X через пробел. Если ограничений по оси нет, введи слово None.'
        answer += 'Для обозначения бесконечностей используй -оо или +оо.\n\n'
        answer += 'Например:\n-100 100'
        self.user.update_status('interval_x')
        self.set_message(answer)

    def handler_interval_x(self):
        try:
            interval_x = handler_input_data.handler.check_limits(self.message)
            BotDatabase().update_query((interval_x, self.user_id), column='interval_x', table='data')
            answer = "Всё окей!\n\n"
            answer += 'Введи ограничения по оси Y через пробел. Если ограничений по оси нет, введи слово None.'
            answer += 'Для обозначения бесконечностей используй -оо или +оо.\n\n'
            answer += 'Например:\n-100 100'
            self.user.update_status('interval_y')
            self.set_message(answer)
        except ValueError as error:
            self.handler_error(error)

    def handler_interval_y(self):
        try:
            interval_y = handler_input_data.handler.check_limits(self.message)
            BotDatabase().update_query((interval_y, self.user_id), column='interval_y', table='data')
            if self.task == 1:
                answer = "Всё окей!\n\nЖдем результат..."
                self.set_message(answer)
                return self.handler_local_extr_res()
            else:
                answer = "Всё окей!\n\nЖдем результат..."
                self.set_message(answer)
                return self.handler_local_extr_with_rest_res()
        except ValueError as error:
            self.handler_error(error)

    def handler_local_extr_res(self):
        self.user.update_status('menu')
        vars, func, restr = BotDatabase().select_query(SELECT_DATA.format('vars, func, restr'), (self.user_id,))
        print(restr)
        if restr == 1:
            interval_x, interval_y = BotDatabase().select_query(SELECT_DATA.format('interval_x, interval_y'),
                                                                (self.user_id, ))
            if interval_x != 'None' and interval_y != 'None':
                task = LocalExtr(vars, func, restr, interval_x=interval_x, interval_y=interval_y)
            elif interval_x == 'None':
                task = LocalExtr(vars, func, restr, interval_y=interval_y)
            elif interval_y == 'None':
                task = LocalExtr(vars, func, restr, interval_x=interval_x)
        else:
            task = LocalExtr(vars, func, restr)
        result = task.solve()
        result += 'График функции можно открыть по ссылке: http://127.0.0.1:5000/'
        self.set_message(result)

    def handler_local_extr_with_rest_res(self):
        self.user.update_status('menu')
        vars, func, g_func, restr = BotDatabase().select_query(SELECT_DATA.format('vars, func, g_func, restr'),
                                                               (self.user_id,))
        if restr == 1:
            interval_x, interval_y = BotDatabase().select_query(SELECT_DATA.format('interval_x, interval_y'),
                                                                (self.user_id,))
            if interval_x != 'None' and interval_y != 'None':
                task = LocalExtrWithRestrictions(vars, func, g_func, restr, interval_x=interval_x, interval_y=interval_y)
            elif interval_x == 'None':
                task = LocalExtrWithRestrictions(vars, func, g_func, restr, interval_y=interval_y)
            elif interval_y == 'None':
                task = LocalExtrWithRestrictions(vars, func, g_func, restr, interval_x=interval_x)
        else:
            task = LocalExtrWithRestrictions(vars, func, g_func, restr)
        result = task.solve()
        result += '\nГрафик функции можно открыть по ссылке: http://127.0.0.1:5000/'
        self.set_message(result)

    def handler_error(self, error):
        answer = f'Введенные данные вызвали ошибку: {error.__str__()}.\nПопробуйте ещё раз!'
        self.set_message(answer)
