import datetime

from bot.utils.menu_utils.epic_games_utils import manage_free_games
from bot.utils.db_api.models_peewee import (
    db,
    Utility
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def plug_func():
    print('plug func')


def set_bot_schedule(scheduler: AsyncIOScheduler):
    current_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    scheduler.add_job(manage_free_games, 'date', run_date=current_time, id='epic_job')
    scheduler.start()
    with db:
        Utility.delete().execute()
    print("расписание составлено")
