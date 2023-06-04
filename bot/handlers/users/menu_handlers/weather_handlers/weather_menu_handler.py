from bot.loader import dp

from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.weather_keyboards import (
    first_level_weather_keyboard
)

from bot.states.menu_states import WeatherState
from bot.utils.menu_utils.work_with_qr import generate_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category=["current_weather_back", "weather"],
                                                      menu_level="1"))
async def choose_weather_period(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    await call.message.edit_text("Выберите тип погоды", reply_markup=first_level_weather_keyboard)
