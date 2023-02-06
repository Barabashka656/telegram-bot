import datetime

from utils.menu_utils.epic_games_utils import write_to_database
from utils.db_api.models_peewee import (
    db,
    Utility
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def plug_func():
    print('plug func')


def set_bot_schedule(scheduler: AsyncIOScheduler):
    current_time = datetime.datetime.now() + datetime.timedelta(seconds=1)
    scheduler.add_job(write_to_database, 'date', run_date=current_time, id='epic_job')
    scheduler.start()
    with db:
        Utility.delete().execute()
    print("расписание составлено")
