import logging

from bot.loader import dp

from aiogram.utils.exceptions import BotBlocked
from aiogram import types

logger = logging.getLogger(__name__)


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked_handler(update: types.Update, exception: BotBlocked) -> bool:
    print('BotBlocked', exception, '\n\n')
    print('Update', update)
    return
