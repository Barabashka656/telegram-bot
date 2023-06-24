import logging

from bot.loader import dp

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

logger = logging.getLogger(__name__)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))
