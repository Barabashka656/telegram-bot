from bot.loader import dp

from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.weather_keyboards import (
    first_level_weather_keyboard,
    current_weather_choose_service_keyboard,
    accu_weather_keyboard
)
from bot.utils.db_api.models_peewee import (
    db,
    WeatherTable,
    WeatherCityId,
    VipUser
)
from bot.states.menu_states import WeatherState
from bot.utils.menu_utils.weather_utils import (
    AccuWeather,
    get_city_id,
    get_current_accu_weather,
    processing
)
from bot.filters import (
    IsAccuWeatherFilter,
    IsVisualWeatherFilter,
    IsTomorrowWeatherFilter,
    # IsWeatherPremiumFilter,
    IsFirstCurrentWeatherUseFilter,
    IsCurrentCityNotInDatabase
)

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsFirstCurrentWeatherUseFilter())
async def first_current_weather_use_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)

    answer_text = "Выберите сервис, который будет предоставлять вам погоду\n\n"\
                  "—> [AccuWeather](https://www.accuweather.com)\n"\
                  "—> [Visual Weather](https://www.iblsoft.com/products/visualweather)\n"\
                  "—> [Tomorrow.io](https://www.tomorrow.io/)"

    await call.message.edit_text(text=answer_text,
                                 reply_markup=current_weather_choose_service_keyboard,
                                 parse_mode="Markdown",
                                 disable_web_page_preview=True)

    await WeatherState.city_data.set()


# Accu handlers ---------------------------------------------------------------------------------------

@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsAccuWeatherFilter(), IsCurrentCityNotInDatabase())
async def weather_accu_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    #    get_current_accu_weather()
    await call.message.edit_text("Введите название города")
    await WeatherState.city_data.set()


@dp.message_handler(state=WeatherState.city_data)
async def send_qr(message: types.Message, state: FSMContext):
    city = message.text  # TODO(check): check city
    print(city)
    with db:
        WeatherTable.update(
            current_weather_city=city
        ).where(
            WeatherTable.user_id == message.from_user.id
        ).execute()

    await state.finish()


@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsAccuWeatherFilter())
async def weather_accu_handler2(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    with db:
        user = WeatherTable.get_or_none(user_id=call.from_user.id)
        city = user.current_weather_city
        city_id = WeatherCityId.get_or_none(city_name=city)
        if city_id:
            city_id = city_id.city_id
        else:
            city_id = get_city_id(city)
            WeatherCityId(
                city_name=city,
                city_id=city_id
            ).save()

    raw_accu_weather = get_current_accu_weather(city_id)
    weather_object = AccuWeather(**raw_accu_weather)
    print(weather_object)

    weather_text = processing(weather_object, True)
    keyboard = accu_weather_keyboard(weather_object.link)

    await call.message.edit_text(weather_text, reply_markup=keyboard)


# accu_current_weather set up
@dp.callback_query_handler(start_menu_callback.filter(category="current_accu_setup", menu_level="3"))
async def accu_weather_setup_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    service = "accu"
    with db:
        vip_user = VipUser.get_or_none(user_id=call.from_user.id)
        if not vip_user:
            vip_user = VipUser(user_id=call.from_user.id).save()

        user = WeatherTable.get_or_none(user_id=call.from_user.id)
        if not user:
            WeatherTable(user_id=call.from_user.id,
                         current_weather_service=service,
                         vip_user_id=vip_user
                         ).save()
        else:
            WeatherTable.update(
                current_weather_service=service
            ).where(WeatherTable.user_id == call.from_user.id)
    answer_text = "Вы выбрали сервис погоды AccuWeather"
    await call.message.edit_text(text=answer_text, reply_markup=first_level_weather_keyboard)


# Visual handlers ---------------------------------------------------------------------------------------

@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsVisualWeatherFilter())
async def weather_visual_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    await call.message.edit_text("3", reply_markup=first_level_weather_keyboard)


# visual_current_weather set up
@dp.callback_query_handler(start_menu_callback.filter(category="current_visual_setup", menu_level="3"))
async def visual_weather_setup_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    await call.message.edit_text("3", reply_markup=first_level_weather_keyboard)


# Tomorrow handlers --------------------------------------------------------------------------------------

@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsTomorrowWeatherFilter())
async def weather_tomorrow_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    await call.message.edit_text("4", reply_markup=first_level_weather_keyboard)


# tommorow_current_weather set up
@dp.callback_query_handler(start_menu_callback.filter(category="current_tomorrow_setup", menu_level="3"))
async def tommorow_weather_setup_handler(call: types.CallbackQuery):  # TODO(rename): func
    await call.answer(cache_time=0)
    await call.message.edit_text("4", reply_markup=first_level_weather_keyboard)
