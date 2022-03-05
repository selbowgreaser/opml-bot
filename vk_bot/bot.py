from vk_api.longpoll import VkEventType

from vk_bot.database import BotDatabase
from vk import VK
from vk_bot.user import User
from vk_bot.answerer.task_manager import TaskManager


def start_work():
    """
    Подключение к сессии, прослушивание longpoll и обработка событий.
    """

    vk = VK()
    print('Бот снова работает...')
    for event in vk.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('Получено новое сообщение!')
            print(f'{event.user_id}: {event.text}')
            db = BotDatabase()
            user = User(vk.vk_api_method, db, event.user_id)
            TaskManager(vk.vk_api_method, db, user, event.text).manage()
        print('Сообщение успешно обработано!')


if __name__ == "__main__":
    start_work()
