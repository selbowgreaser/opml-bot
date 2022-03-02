from vk_get_api import VKApi
from database import BotDatabase


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.first_name = VKApi().vk.users.get(user_id=user_id)[0]['first_name']
        self.last_name = VKApi().vk.users.get(user_id=user_id)[0]['last_name']

    def authorization(self):
        if not BotDatabase().select_query('SELECT user_id FROM users WHERE user_id = ?', (self.user_id,)):
            self.registration()
        return (self.first_name,
                BotDatabase().select_query('SELECT status FROM users WHERE user_id = ?', (self.user_id,))[0])

    def registration(self):
        BotDatabase().insert_query('users', (self.user_id, self.first_name, self.last_name))
        BotDatabase().insert_query('data', (self.user_id, ))

    def update_status(self, status):
        BotDatabase().update_query((status, self.user_id))