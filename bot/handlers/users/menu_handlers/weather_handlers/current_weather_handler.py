import typing

from bot.loader import dp
from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.weather_keyboards import (
    first_level_weather_keyboard,
    current_weather_choose_service_keyboard,
    create_weather_keyboard
)
from bot.keyboards.inline.menu_keyboards.menu_buttoms import menu_newmsg_back_keyboard
from bot.utils.db_api.models_peewee import (
    db,
    WeatherTable,
    WeatherCityId,
    VipUser
)
from bot.states.menu_states import WeatherState
from bot.utils.menu_utils.weather_utils.weather_processing import weather_processing_overview
from bot.utils.menu_utils.weather_utils.get_current_weather_util import (
    get_current_weather,
    WeatherHandledTuple
)
from bot.filters import (
    IsAccuWeatherFilter,
    IsVisualWeatherFilter,
    IsTomorrowWeatherFilter,
    # IsWeatherPremiumFilter,
    IsFirstCurrentWeatherUseFilter,
    IsCurrentCityNotInDatabase
)
from bot.utils.custom_bot_exceptions import (
    InvalidWeatherServiceError,
    InvalidResponseStatusCodeError,
    InvalidCityNameError
)

import asyncio
from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(start_menu_callback.filter(category="update_db_with_current_service", menu_level="2"))
@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"),
                           IsFirstCurrentWeatherUseFilter())
async def first_current_weather_use_handler(call: types.CallbackQuery):
    await call.answer(cache_time=0)

    answer_text = "Выберите сервис, который будет предоставлять вам погоду\n\n"\
                  "—> [AccuWeather](https://www.accuweather.com)\n"\
                  "—> [Visual Weather](https://www.iblsoft.com/products/visualweather)\n"\
                  "—> [Tomorrow.io](https://www.tomorrow.io/)"

    await call.message.edit_text(text=answer_text,
                                 reply_markup=current_weather_choose_service_keyboard,
                                 parse_mode="Markdown",
                                 disable_web_page_preview=True)


@dp.callback_query_handler(
        start_menu_callback.filter(
        category=["current_accu_setup", "current_visual_setup", "current_tomorrow_setup"], 
        menu_level="3")
    )
async def current_weather_setup_handler(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    service = call.data.split('_')[1]
    with db:
        vip_user = VipUser.get_or_none(user_id=call.from_user.id)
        if not vip_user:
            vip_user = VipUser(user_id=call.from_user.id).save()
            
        user = WeatherTable.get_or_none(user_id=call.from_user.id)
        answer_text = f'Вы выбрали сервис погоды "{service}"'
        if user:
            WeatherTable.update(
                current_weather_service=service
            ).where(WeatherTable.user_id == call.from_user.id
            ).execute()
            city = user.current_weather_service

            if city:
                return await call.message.edit_text(text=answer_text, reply_markup=first_level_weather_keyboard)
        else:
            WeatherTable(user_id=call.from_user.id,
                         current_weather_service=service,
                         vip_user_id=vip_user
                         ).save()
            
    answer_text = f'Вы выбрали сервис погоды "{service}"'
    await call.message.answer(text=answer_text)
    await weather_city_handler(call=call, is_call_from_func=True)


@dp.callback_query_handler(
        start_menu_callback.filter(
        category="current_weather",
        menu_level="2"),
        IsCurrentCityNotInDatabase()
    )
@dp.callback_query_handler(start_menu_callback.filter(category="update_db_with_current_city",
                                                      menu_level="2"))
async def weather_city_handler(call: types.CallbackQuery, is_call_from_func: bool = False):  
    await call.answer(cache_time=0)
    if is_call_from_func:
        await call.message.answer("Введите название города")
    else:
        await call.message.edit_text("Введите название города")
    await WeatherState.city_data.set() 


@dp.message_handler(state=WeatherState.city_data)
async def update_db_with_city(message: types.Message, state: FSMContext):
    city = message.text  # TODO(check): check the city
    print(city)
    with db:
        WeatherTable.update(
            city_name=city
        ).where(
            WeatherTable.user_id == message.from_user.id
        ).execute()

    await state.finish()

    answer_text = "Вы выбрали свой город"
    await message.answer(text=answer_text, reply_markup=first_level_weather_keyboard)


# qweqwe
@dp.callback_query_handler(start_menu_callback.filter(category="current_weather", menu_level="2"))
async def weather_handler_overview(call: types.CallbackQuery, state: FSMContext): 
    await call.answer(cache_time=0)
    
    try:
        weather_object: WeatherHandledTuple = await get_current_weather(call=call)
    except InvalidWeatherServiceError as e:
        print(e)
        answer_text = 'Произошла ошибка (weather:error 210)'
        return await call.message.edit_text(text=answer_text, 
                                            reply_markup=menu_newmsg_back_keyboard)
    except InvalidResponseStatusCodeError as e:
        print(e)
        answer_text = 'Произошла ошибка (weather:error 211)'
        return await call.message.edit_text(text=answer_text, 
                                            reply_markup=menu_newmsg_back_keyboard)
    except InvalidCityNameError as e:
        answer_text = 'Произошла ошибка (weather:error 213)' + f'\nгород "{e.message}" неверный'
        WeatherTable.update(
            city_name=None
        ).where(WeatherTable.user_id == call.from_user.id).execute()
        await call.message.answer(text=answer_text, reply_markup=menu_newmsg_back_keyboard)
        await asyncio.sleep(0.3)
        await weather_city_handler(call=call, is_call_from_func=True)
        return 
    
    print(weather_object)

    
    keyboard = create_weather_keyboard(weather_link=weather_object.accu_link)
    
    async with state.proxy() as data:
        data['current_weather_detail'] = weather_object.detail
    await call.message.edit_text(text=weather_object.overview, reply_markup=keyboard)


@dp.callback_query_handler(start_menu_callback.filter(category="current_weather_detail"))
async def weather_accu_handler_detail(call: types.CallbackQuery, state: FSMContext):  # TODO(rename): func
    await call.answer(cache_time=0)

    async with state.proxy() as data:
        weather_text = data.get('current_weather_detail')
        await call.message.edit_text(text=weather_text, reply_markup=menu_newmsg_back_keyboard)
        await state.finish()
