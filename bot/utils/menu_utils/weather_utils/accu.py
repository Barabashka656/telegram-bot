from bot.data.config import ACCU_WEATHER_API_KEY
from bot.utils.custom_bot_exceptions import (
    InvalidResponseStatusCodeError,
    InvalidCityNameError
)

import aiohttp


async def get_accu_city_id(city: str) -> str:
    language = 'ru'
    url = "http://dataservice.accuweather.com/locations/v1/cities/autocomplete" +\
          f"?apikey={ACCU_WEATHER_API_KEY}" + \
          f"&q={city}" + \
          f"&language={language}"

    async with aiohttp.ClientSession() as client:
        async with client.get(url=url) as response:
            match response.status:
                case 200:
                    data = await response.json()
                    if not data:
                        raise InvalidCityNameError(city)
                    return data[0]['Key']
                case _:
                    raise InvalidResponseStatusCodeError(response)


async def get_current_accu_weather(city_id: str) -> dict:

    url = "http://dataservice.accuweather.com/currentconditions/v1" +\
          f"/{city_id}" +\
          f"?apikey={ACCU_WEATHER_API_KEY}" +\
          "&language=ru-ru" +\
          "&details=true"

    async with aiohttp.ClientSession() as client:
        async with client.get(url=url) as response:
            match response.status:
                case 200:
                    data = await response.json()
                    return data[0]
                case _:
                    raise InvalidResponseStatusCodeError(response)
