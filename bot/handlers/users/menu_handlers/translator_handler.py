import logging

from bot.keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from bot.loader import dp

from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)


@dp.callback_query_handler(start_menu_callback.filter(category="translator"))
async def buying_pear(call: CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer("Переводчик")  # reply_markup=)
