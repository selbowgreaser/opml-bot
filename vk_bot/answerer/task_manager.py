from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.message_handlers import Handlers
from vk_bot.answerer.response_init import Response
from vk_bot.database import BotDatabase
from vk_bot.user import User


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
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User):
        self.vk = vk_api_method
        self.db = db
        self.user = user
        self.status = user.authorization()
        self.handlers = Handlers(vk_api_method, db, user)
        # возможно есть смысл добавить аттрибут task

    def manage(self, text: str) -> Response:
        """
        Управление обработкой входящих сообщений. Необходим для разделения задач на различные пакеты.

        Parameters
        ----------
        text : str
            Текст сообщения, отправленного пользователем.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        if self.status == 'start':
            return self.handlers.greetings(self.user.get_first_name())

        if self.status == 'greetings':
            if text == 'Меню':
                return self.handlers.menu()
            if text == 'Обо мне':
                return self.handlers.about_me()
            return self.handlers.click_button()

        if self.status == 'about_me':
            if text == 'Меню':
                return self.handlers.menu()
            return self.handlers.click_button()

        if self.status == 'menu':
            if text == 'Поиск экстремума':
                pass
            if text == 'Обо мне':
                return self.handlers.about_me()
