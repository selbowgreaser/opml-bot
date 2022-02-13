from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_bot.user import User
from vk_get_api import VKApi


class Handler:
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.name, self.status = User(user_id).authorization().values()

    def get_message(self, answer, keyboard=None):
        answer = answer
        keyboard = keyboard
        return VKApi().send_message(self.user_id, answer, keyboard)

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

    def handler_welcome(self):
        answer = f"Привет, {self.name}!\n\nНажми на кнопочку!"
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("МЕНЮ", color=VkKeyboardColor.POSITIVE)
        self.get_message(answer, keyboard.get_keyboard())

    def handler_menu(self):
        User(self.user_id).update_status('menu')
        answer = f"Возможности бота:\n\n" \
                 f"1. Найти локальный экстремум функции двух переменных\n" \
                 f"2. Найти локальный экстремум функции двух переменных с ограничениями (методом Лагранжа)"
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("1", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("2", color=VkKeyboardColor.POSITIVE)
        self.get_message(answer, keyboard.get_keyboard())

    def handler_local_extr(self):
        pass

    def handler_local_extr_with_rest(self):
        pass




