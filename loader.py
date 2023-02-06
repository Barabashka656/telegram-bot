from data.config import TELEGRAM_API_TOKEN

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import pyshorteners


shortcut_object = pyshorteners.Shortener()
bot = Bot(TELEGRAM_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone='Europe/Minsk')
