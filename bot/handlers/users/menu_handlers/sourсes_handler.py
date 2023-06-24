import logging
from bot.loader import dp
from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.menu_buttoms\
    import my_sources_keyboard

from aiogram import types

logger = logging.getLogger(__name__)


@dp.callback_query_handler(start_menu_callback.filter(category="sources"))
async def show_sources(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.edit_text("Ресурсы", reply_markup=my_sources_keyboard)
