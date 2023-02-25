from bot.data.config import ACCU_WEATHER_API_KEY
from bot.utils.custom_bot_exceptions import InvalidResponseStatusCodeError

import requests


def get_city_id(city: str) -> str:
    id_url = "http://dataservice.accuweather.com/locations/v1/cities/autocomplete" +\
             f"?apikey={ACCU_WEATHER_API_KEY}" + \
             f"&q={city}"

    print(id_url)
    response = requests.get(url=id_url)
    match response.status_code:
        case 200:
            return response.json()[0]['Key']
        case _:
            raise InvalidResponseStatusCodeError(response)


def get_current_accu_weather(city_id: str) -> dict:

    url = "http://dataservice.accuweather.com/currentconditions/v1" +\
          f"/{city_id}" +\
          f"?apikey={ACCU_WEATHER_API_KEY}" +\
          "&language=ru-ru" +\
          "&details=true"

    response = requests.get(url=url)
    match response.status_code:
        case 200:
            return response.json()[0]
        case _:
            raise InvalidResponseStatusCodeError(response)
