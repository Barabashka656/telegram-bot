import logging

from bot.utils.db_api.models_peewee import (
    db,
    VipUser,
    WeatherTable
)

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


logger = logging.getLogger(__name__)


class IsCurrentCityNotInDatabase(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        with db:
            user = WeatherTable.select(
                WeatherTable.city_name
            ).where(
                (WeatherTable.user_id == call.message.chat.id)
                & WeatherTable.city_name.is_null(False)
            )
            return not len(user)


class IsFirstCurrentWeatherUseFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        with db:
            user = WeatherTable.get_or_none(user_id=call.message.chat.id)
            return not user or not user.current_weather_service


class IsWeatherPremiumFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        with db:
            return VipUser.get_or_none(user_id=call.message.chat.id, is_weather_premium=True)


class IsAccuWeatherFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        service = "accu"
        with db:
            user = WeatherTable.get_or_none(user_id=call.message.chat.id, current_weather_service=service)
        return user


class IsVisualWeatherFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        service = "visual"
        with db:
            user = WeatherTable.get_or_none(user_id=call.message.chat.id, current_weather_service=service)
        return user


class IsTomorrowWeatherFilter(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        service = "tomorrow"
        with db:
            user = WeatherTable.get_or_none(user_id=call.message.chat.id, current_weather_service=service)
        return user
