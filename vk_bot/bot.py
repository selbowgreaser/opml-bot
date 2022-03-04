from vk_get_api import VKApi
from messages import Handler

from vk_api.longpoll import VkEventType


def start_work():
    vk = VKApi()

    for event in vk.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('***NEW MESSAGE***')
            print(f'{event.user_id}: {event.text}')
            Handler(vk, event.user_id, event.text).story()


if __name__ == "__main__":
    start_work()
