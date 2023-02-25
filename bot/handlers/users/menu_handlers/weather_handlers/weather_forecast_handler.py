from bot.loader import dp

from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.weather_keyboards\
    import first_level_weather_keyboard
from bot.states.menu_states import WeatherState
from bot.utils.menu_utils import generate_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram import types
