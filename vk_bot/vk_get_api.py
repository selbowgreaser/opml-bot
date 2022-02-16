from config import ACCESS_TOKEN, GROUP_ID, API_VERSION

import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll
from vk_api.upload import VkUpload


class VKApi:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=ACCESS_TOKEN,
                                       api_version=API_VERSION)
        self.longpoll = VkLongPoll(self.vk_session,
                                   group_id=GROUP_ID)
        self.vk = self.vk_session.get_api()
        self.upload = VkUpload(self.vk)

    def send_message(self, user_id, answer, attachment, keyboard):
        self.vk.messages.send(user_id=user_id,
                              random_id=get_random_id(),
                              message=answer,
                              attachment=attachment,
                              keyboard=keyboard)

    def upload_photo(self, photo):
        response = self.upload.photo_messages(photo)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']

        return f'photo{owner_id}_{photo_id}_{access_key}'
