import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Telegram API конфигурация
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "")

# Путь к файлу сессии
SESSION_NAME = "userbot_session"

# Настройки бота
DEBUG = os.getenv("DEBUG", "False").lower() == "true"