from vk_bot.answerer.task_manager import TaskManager
from vk_bot.database import BotDatabase
from vk_bot.user import User
from vk_bot.vk import VK


class MainHandler:
    """
    Главный обработчик сообщений пользователей.

    Parameters
    ----------
    data : dict
        Данные из запроса сервера.
    """

    def __init__(self, data: dict):
        self.request_data = data
        self.user_id = self.get_user_id()
        self.text = self.get_text()

    def get_user_id(self) -> int:
        """
        Получение user_id из запроса.

        Returns
        -------
        int
            id пользвателя, от которого пришло сообщение боту.
        """

        return self.request_data["object"]["message"]["from_id"]

    def get_text(self) -> str:
        """
        Получение text из запроса.

        Returns
        -------
        str
            Текст сообщения пользвателя.
        """

        return self.request_data["object"]["message"]["text"]

    def process(self):
        """
        Запуск процесса обработки сообщения.
        """

        print('Получено новое сообщение!')
        print(f'{self.user_id}: {self.text}')
        vk = VK()
        db = BotDatabase()
        user = User(vk.vk_api_method, db, self.user_id)
        tm = TaskManager(vk.vk_api_method, db, user)
        reply = tm.manage(self.text)
        message = reply.get_message()
        vk.send_message(message)
        print('Сообщение успешно обработано!')
