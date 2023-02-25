from bot.utils.db_api.models_peewee import (
    db,
    VipUser,
    WeatherTable
)

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class IsCurrentCityNotInDatabase(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        with db:
            user = WeatherTable.select(
                WeatherTable.current_weather_city
            ).where(
                (WeatherTable.user_id == call.message.chat.id)
                & WeatherTable.current_weather_city.is_null(False)
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
            print(VipUser.get_or_none(user_id=call.message.chat.id, is_weather_premium=True))
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
