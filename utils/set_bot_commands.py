from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(dp: Dispatcher):

    STARTING_COMMANDS = {
        'en': [
            BotCommand('start', "run bot"),
            BotCommand('help', "HELP ME!!")
        ],
        'ru': [
            BotCommand('start', "запустить бота"),
            BotCommand('help', "ПОМОГИТЕ!!")
        ]

    }
    for current_language_code, current_commands in STARTING_COMMANDS.items():
        await dp.bot.set_my_commands(
            commands=current_commands,
            scope=BotCommandScopeDefault(),
            language_code=current_language_code
        )
