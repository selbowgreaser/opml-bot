from vk_bot.user import User
from vk_get_api import VKApi


class Handler:
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.name, self.status = User(user_id).authorization().values()

    def send_message(self, answer, keyboard=None):
        answer = answer
        keyboard = keyboard
        return VKApi().send_message(self.user_id, answer, keyboard)

    def story(self):
        if self.status == 'welcome':
            answer = f"Привет, {self.name}"
            VKApi().send_message(self.user_id, answer, keyboard=None)



