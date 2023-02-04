import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
STORAGE_DIR = os.getenv('STORAGE_DIR')
DATABASE_DIR = os.getenv('DATABASE_DIR')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

DISCORD_INVITE_LINK = os.getenv('DISCORD_INVITE_LINK')
TELEGRAM_LINK = os.getenv('TELEGRAM_LINK')