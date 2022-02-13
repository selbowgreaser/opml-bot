from vk_get_api import VKApi
from database import BotDatabase


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.first_name = VKApi().vk.users.get(user_id=user_id)[0]['first_name']
        self.last_name = VKApi().vk.users.get(user_id=user_id)[0]['last_name']

    def authorization(self):
        if not BotDatabase().select_query('SELECT user_id FROM users WHERE user_id = ?', (self.user_id, )):
            self.registration()
        return {"name": self.first_name,
                "status": BotDatabase().select_query('SELECT status FROM users WHERE user_id = ?', (self.user_id, ))[0][0]}

    def registration(self):
        BotDatabase().insert_query((self.user_id, self.first_name, self.last_name))

    def update_status(self, status):
        BotDatabase().update_query((status, self.user_id))
