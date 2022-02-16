import sympy
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from LocalExtrWithRestrictions import LocalExtrWithRestrictions
from vk_bot.user import User
from vk_get_api import VKApi


class Handler:
    def __init__(self, vk, user_id, message):
        self.vk = vk
        self.user = User(user_id)
        self.user_id = user_id
        self.message = message
        self.name, self.status = self.user.authorization()

    def get_message(self, answer, keyboard=None, attachment=None,):
        answer = answer
        keyboard = keyboard
        return self.vk.send_message(self.user_id, answer, attachment, keyboard)

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
            if self.message == "НАЗАД":
                return self.handler_menu()

        if self.status == '2':
            if self.message == "НАЗАД":
                return self.handler_menu()
            return self.handler_variables()
        if self.status == '2.1':
            return self.handler_functions()
        if self.status == '2.2':
            return self.handler_g_functions()
        if self.status == '2.3':
            return self.handler_lewr_result()

    def handler_welcome(self):
        answer = f"Привет, {self.name}!\n\nНажми на кнопочку!"
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("МЕНЮ", color=VkKeyboardColor.POSITIVE)
        self.get_message(answer, keyboard.get_keyboard())

    def handler_menu(self):
        self.user.update_status('menu')
        answer = f"Возможности бота:\n\n" \
                 f"1. Найти локальный экстремум функции двух переменных\n" \
                 f"2. Найти локальный экстремум функции двух переменных с ограничениями (методом Лагранжа)"
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("1", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("2", color=VkKeyboardColor.POSITIVE)
        self.get_message(answer, keyboard.get_keyboard())

    def handler_local_extr(self):
        self.user.update_status('1')
        answer = "-_- Тут пока ничего нет -_-"
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("НАЗАД", color=VkKeyboardColor.POSITIVE)
        self.get_message(answer, keyboard.get_keyboard())

    def handler_local_extr_with_rest(self):
        self.user.update_status('2.3')
        answer = "Введите все входные данные, начиная с новой строки"
        self.get_message(answer)

    def handler_lewr_result(self):
        self.user.update_status('menu')
        variables, func, g_func = self.message.split('\n')
        variables = variables.split()
        func = sympy.sympify(func)
        g_func = sympy.sympify(g_func)
        task = LocalExtrWithRestrictions(variables, func, g_func, restr=False)
        result = task.solve()
        graph = self.vk.upload_photo('graph.png')
        self.get_message(result, attachment=graph)
