import json
import os
from urllib import request

from flask import Flask

from vk_bot.config import CONFIRMATION_TOKEN
from vk_bot.main_handler import MainHandler

app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN
    elif data['type'] == 'message_new':
        MainHandler(data).process()
        return 'ok'


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
