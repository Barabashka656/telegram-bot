import os

from dotenv import find_dotenv, load_dotenv
UPDATE_DATABASE = False  # set True to update database

load_dotenv(find_dotenv())
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
STORAGE_PATH = os.path.join('bot', 'data', 'file_storage')

DISCORD_INVITE_LINK = os.getenv('DISCORD_INVITE_LINK')
TELEGRAM_LINK = os.getenv('TELEGRAM_LINK')

ACCU_WEATHER_API_KEY = os.getenv('ACCU_WEATHER_API_KEY')
TOMORROW_IO_API_KEY = os.getenv('TOMORROW_IO_API_KEY')
VISUAL_API_KEY = os.getenv('VISUAL_API_KEY')

DATABASE_PATH = os.path.join('bot', 'data', 'Databases', 'bot_database.db')
