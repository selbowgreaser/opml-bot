from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id


class Response:
    """
    Сообщение для пользователя.

    Parameters
    ----------
    user_id: int
        id пользователя, которому будет отправлен ответ.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.random_id = get_random_id()
        self.text = ''
        self.keyboard = None

    def set_text(self, text: str):
        """
        Установка текстового ответа.

        Parameters
        ----------
        text : str
            Текст ответа.
        """

        self.text = text

    def set_keyboard(self, keyboard: VkKeyboard):
        """
        Установка клавиатуры.

        Parameters
        ----------
        keyboard : VkKeyboard
            Объект клавиатуры.
        """

        self.keyboard = keyboard.get_keyboard()

    def get_message(self) -> dict:
        """
        Формирование словаря с параметрами сообщения для отправки сообщения пользователю.

        Returns
        -------
        dict
            Параметры для метода send_message, которые необходимы для отправки сообщения c помощью API VK.
        """

        parameters = {"user_id": self.user_id,
                      "random_id": self.random_id,
                      "message": self.text}

        if self.keyboard:
            parameters.update(keyboard=self.keyboard)

        return parameters
