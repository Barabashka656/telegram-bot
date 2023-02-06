from loader import dp
from utils.db_api.models_peewee import (
    db,
    EpicMail
)
from keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import (
    epic_sub_settings_buttom,
    epic_cancel_settings_buttom,
    menu_editmsg_buttom
)


from aiogram import types
from aiogram.types import InlineKeyboardMarkup


@dp.callback_query_handler(start_menu_callback.filter(category="settings"))
async def show_sources(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    settings_keyboard = InlineKeyboardMarkup(row_width=1)
    with db:
        if EpicMail.get_or_none(user_id=call.from_user.id):
            settings_keyboard.insert(epic_cancel_settings_buttom)
        else:
            settings_keyboard.insert(epic_sub_settings_buttom)
    settings_keyboard.insert(menu_editmsg_buttom)
    answer_text = "Настройки бота"
    await call.message.edit_text(text=answer_text,
                                 reply_markup=settings_keyboard)
