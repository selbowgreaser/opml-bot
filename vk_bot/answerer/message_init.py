from typing import Optional

from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id


class Message:
    """
    Сообщение для пользователя.

    Parameters
    ----------
    user_id: int
        id пользователя, которому будет отправлен ответ
    text: str
        Ответ пользователю в виде строки
    keyboard: VkKeyboard
        Объект клавиатуры для пользователя
    """

    def __init__(self, user_id: int, text: str, keyboard: Optional[VkKeyboard] = None):
        self.user_id = user_id
        self.random_id = get_random_id()
        self.text = text
        self.keyboard = keyboard

    def get_message(self) -> dict:
        """
        Формирование словаря с параметрами сообщения для отправки сообщения пользователю.

        Returns
        -------
        dict
            Параметры для метода send_message, которые необходимы для отправки сообщения c помощью api VK.
        """

        parameters = {"user_id": self.user_id,
                      "random_id": self.random_id,
                      "message": self.text}

        if self.keyboard:
            parameters.update(keyboard=self.keyboard)

        return parameters
