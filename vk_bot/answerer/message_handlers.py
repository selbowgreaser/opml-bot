from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.task_manager import TaskManager
from vk_bot.database import BotDatabase
from vk_bot.user import User


class Handlers(TaskManager):
    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User):
        super().__init__(vk_api_method, db, user, )

    def welcome(self, first_name):
        pass
