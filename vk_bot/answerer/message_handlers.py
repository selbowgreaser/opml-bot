from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.keyboards import Keyboards
from vk_bot.answerer.response_init import Response
from vk_bot.answerer.scripted_phrases import Phrases
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

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User):
        self.vk = vk_api_method
        self.db = db
        self.user = user
        self.response = Response(self.user.user_id)

    def greetings(self, first_name: str) -> Response:
        """
        Приветствие пользователя и вывод стартовой клавиатуры.
        Статус: greetings

        Parameters
        ----------
        first_name : str
            Имя пользователя.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        self.user.update_status('greetings')
        self.response.set_text(Phrases.GREETINGS.format(first_name))
        self.response.set_keyboard(Keyboards().for_welcome())
        return self.response

    def about_me(self) -> Response:
        """
        Информация о боте и его разработчиках.
        Статус: about_me

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.user.update_status('about_me')
        self.response.set_text(Phrases.ABOUT_ME)
        self.response.set_keyboard(Keyboards().for_about_me())
        return self.response

    def menu(self) -> Response:
        """
        Список доступных функций бота.
        Статус: menu

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        self.user.update_status('menu')
        self.response.set_text(Phrases.MENU)
        self.response.set_keyboard(Keyboards().for_menu())
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
