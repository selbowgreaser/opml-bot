import vk_api
from vk_api.longpoll import VkLongPoll

from config import ACCESS_TOKEN, GROUP_ID, API_VERSION


class VKApi:
    """
    Соединение с VK и получение методов API.
    """

    def __init__(self):
        self.vk_session = vk_api.VkApi(token=ACCESS_TOKEN,
                                       api_version=API_VERSION)
        self.longpoll = VkLongPoll(self.vk_session,
                                   group_id=GROUP_ID)
        self.vk = self.vk_session.get_api()

    def send_message(self, parameters):
        """
        Отправка сообщения пользователю с помощью API-метода.

        Parameters
        ----------
        parameters : dict
            Словарь с параметрами, необходимыми для отправки сообщения пользователю.
        """

        self.vk.messages.send(**parameters)
