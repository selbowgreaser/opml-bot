from vk_api.longpoll import VkEventType

from vk_bot.database import BotDatabase
from vk_bot.vk import VK
from vk_bot.user import User
from vk_bot.answerer.task_manager import TaskManager


def start_work():
    """
    Подключение к сессии, прослушивание longpoll и обработка событий.
    """

    vk = VK()
    db = BotDatabase()
    print('Бот снова работает...')
    for event in vk.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('Получено новое сообщение!')
            print(f'{event.user_id}: {event.text}')
            user = User(vk.vk_api_method, db, event.user_id)
            tm = TaskManager(vk.vk_api_method, db, user)
            reply = tm.manage(event.text)
            message = reply.get_message()
            vk.send_message(message)
            print('Сообщение успешно обработано!')


if __name__ == "__main__":
    start_work()
