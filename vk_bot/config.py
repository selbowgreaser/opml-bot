import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.venv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
GROUP_ID = os.environ.get("GROUP_ID")
CONFIRMATION_TOKEN = os.environ.get("CONFIRMATION_TOKEN")
API_VERSION = '5.131'
