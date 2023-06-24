import os.path

from bot.loader import dp, scheduler
from bot.data.config import (
    DATABASE_PATH,
    UPDATE_DATABASE
)
from bot.utils.set_scheduler import set_bot_schedule
from bot.utils.set_bot_commands import set_default_commands
from bot.utils.db_api.models_peewee import create_database
from bot import (
    middlewares,
    filters,
    handlers
)

from aiogram import (
    Dispatcher,
    executor
)


async def set_all_default_commands(dp: Dispatcher):
    await set_default_commands(dp)


def check_database_exist(update_database: bool):
    update_database = True
    if not os.path.exists(DATABASE_PATH) \
       or update_database:
        create_database()


async def on_startup(dp: Dispatcher):
    await set_all_default_commands(dp)

    check_database_exist(UPDATE_DATABASE)

    set_bot_schedule(scheduler)

    print("Ready to start")

if __name__ == "__main__":

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
