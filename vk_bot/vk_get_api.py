from config import ACCESS_TOKEN, GROUP_ID, API_VERSION

import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll


class VKApi:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=ACCESS_TOKEN,
                                       api_version=API_VERSION)
        self.longpoll = VkLongPoll(self.vk_session,
                                   group_id=GROUP_ID)
        self.vk = self.vk_session.get_api()

    def send_message(self, user_id, answer, keyboard):
        self.vk.messages.send(user_id=user_id,
                              random_id=get_random_id(),
                              message=answer,
                              keyboard=keyboard)
