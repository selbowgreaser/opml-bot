from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.message_handlers import Handlers
from vk_bot.database import BotDatabase
from vk_bot.user import User
from vk_bot.vk import VK


class TaskManager:
    """
    Менеджер управления сценарием работы бота.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект соединения с VK и набор методов API.
    db : BotDatabase
        Объект для взаимодействия с базой данных.
    user : User
        Объект для взаимодействия с данными пользователя.
    text : str
        Текст сообщения, отправленного пользователем.
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User, text: str):
        self.vk = vk_api_method
        self.db = db
        self.user = user
        self.status = user.authorization()
        self.text = text
        self.handlers = Handlers(vk_api_method, db, user)
        # возможно есть смысл добавить аттрибут task

    def manage(self):
        if self.status == 'welcome':
            return self.handlers.welcome(self.user.get_first_name())



