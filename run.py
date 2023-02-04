import os.path

from loader import dp, scheduler
from data.config import DATABASE_DIR 
from utils.set_scheduler import set_bot_schedule
from utils.set_bot_commands import set_default_commands
from utils.db_api.models_peewee import create_database
import handlers 

from aiogram import Dispatcher, executor

async def set_all_default_commands(dp: Dispatcher):
    await set_default_commands(dp)

def check_database_exist():
    if not os.path.exists(DATABASE_DIR):
        create_database()



async def on_startup(dp: Dispatcher):
    await set_all_default_commands(dp)

    check_database_exist()
    
    set_bot_schedule(scheduler)
   
 
    
    print("Ready to start")
    

if __name__ == "__main__":
    
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    