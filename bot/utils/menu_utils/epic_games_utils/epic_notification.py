import datetime
import logging

from bot.loader import bot
from bot.utils.db_api.models_peewee import (
    db,
    EpicFreeGame,
    Utility
)
from bot.keyboards.inline.menu_keyboards.menu_buttoms import (
    epic_cancel_newmsg_buttom,
    menu_editmsg_buttom
)

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

logger = logging.getLogger(__name__)


async def show_epic_free_notification(user_id: int):
    games = EpicFreeGame.select()
    for game in games:
        epic_link = InlineKeyboardButton(text="Открыть Epic games", url=game.product_slug)
        epic_store_keyboard = InlineKeyboardMarkup().insert(epic_link)
        await bot.send_photo(chat_id=user_id, photo=game.key_image_url, caption=game.description)

        if game.start_date and game.end_date:
            start_date = datetime.datetime.fromisoformat(game.start_date).strftime("%H:%M %d-%m-%Y")
            end_date = datetime.datetime.fromisoformat(game.end_date).strftime("%H:%M %d-%m-%Y")
            answer_text = f"{game.title}\n Игра бесплатна с {start_date} по {end_date}"
            await bot.send_message(chat_id=user_id, text=answer_text, reply_markup=epic_store_keyboard)
        else:
            await bot.send_message(chat_id=user_id, text=f"{game.title} дата неизвестна",
                                   reply_markup=epic_store_keyboard)
    with db:
        next_notif_date = datetime.datetime.fromisoformat(Utility.get().next_notification).strftime("%H:%M %d-%m-%Y")
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.insert(epic_cancel_newmsg_buttom)
        keyboard.insert(menu_editmsg_buttom)
        answer_text = f"Следующая рассылка будет в {next_notif_date}"
        await bot.send_message(chat_id=user_id, text=answer_text, reply_markup=keyboard)
