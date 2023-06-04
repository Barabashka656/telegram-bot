from typing import NamedTuple

from .visual import get_current_visual_weather
from .tomorrow import get_current_tomorrow_weather
from .accu import (
    get_current_accu_weather,
    get_accu_city_id
)
from .weather_processing import (
    accu_weather_processing,
    tomorrow_weather_processing,
    visual_weather_processing,
    weather_processing_overview
)
from .weather_class import (
    AccuWeather,
    VisualWeather,
    TommorowWeather
)
from bot.utils.custom_bot_exceptions import InvalidWeatherServiceError
from bot.utils.db_api.models_peewee import (
    db,
    WeatherTable,
    WeatherCityId
)

from aiogram import types


class WeatherHandledTuple(NamedTuple):
    overview: str
    detail: str
    accu_link: str = None


async def get_current_weather(call: types.CallbackQuery) -> WeatherHandledTuple:
    city, service = get_service_and_city_from_db(call=call)
    match service:
        case 'accu':
            city_id = await get_city_id_from_db(call=call)
            raw_accu_weather = await get_current_accu_weather(city_id=city_id)
            print('raw', raw_accu_weather)
            weather_object = AccuWeather(**raw_accu_weather)
            print('lel', weather_object)
            weather_text_overview = weather_processing_overview(weather_object)
            weather_text_detal = accu_weather_processing(weather_object)
            return WeatherHandledTuple(weather_text_overview, weather_text_detal, weather_object.link)

        case 'visual':
            raw_visual_weather = await get_current_visual_weather(city=city)
            print(raw_visual_weather)
            weather_object = VisualWeather(**raw_visual_weather)
            print(weather_object)
            weather_text_overview = weather_processing_overview(weather_object)
            weather_text_detal = visual_weather_processing(weather_object)
            return WeatherHandledTuple(weather_text_overview, weather_text_detal)

        case 'tomorrow':
            raw_tommorow_weather = await get_current_tomorrow_weather(city=city)
            print(raw_tommorow_weather)
            weather_object = TommorowWeather(**raw_tommorow_weather)
            print(weather_object)
            weather_text_overview = weather_processing_overview(weather_object)
            weather_text_detal = tomorrow_weather_processing(weather_object)
            return WeatherHandledTuple(weather_text_overview, weather_text_detal)

        case _:
            raise InvalidWeatherServiceError(service)


def get_service_and_city_from_db(call: types.CallbackQuery):
    with db:
        user = WeatherTable.get_or_none(user_id=call.from_user.id)
        city = user.city_name
        service = user.current_weather_service
        return city, service


async def get_city_id_from_db(call: types.CallbackQuery):
    with db:
        user = WeatherTable.get_or_none(user_id=call.from_user.id)
        city = user.city_name
        city_id = WeatherCityId.get_or_none(city_name=city)
        if city_id:
            city_id = city_id.city_id
        else:
            city_id = await get_accu_city_id(city)      # InvalidCityNameError may be raised

            WeatherCityId(
                city_name=city,
                city_id=city_id
            ).save()
        return city_id
