from pprint import pprint

from data.config import ACCU_WEATHER_API
from custom_bot_exceptions import InvalidResponseStatusCodeError

import requests


def get_city_id(city: str) -> str | InvalidResponseStatusCodeError:
    id_url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete\
                ?apikey={ACCU_WEATHER_API}\
                &q={city}\
                &language=en-us"

    response = requests.get(url=id_url)
    match response:
        case 200:
            return response.json()[0]['Key']
        case _:
            raise InvalidResponseStatusCodeError(response)


def get_current_weather(city: str) -> dict | InvalidResponseStatusCodeError:

    city_id = get_city_id(city)     # minsk 28580
    url = f'http://dataservice.accuweather.com/currentconditions/v1\
                    /{city_id}\
                    ?apikey={ACCU_WEATHER_API}\
                    &language=ru-ru\
                    &details=true'

    response = requests.get(url=url)
    match response:
        case 200:
            return response.json()[0]
        case _:
            raise InvalidResponseStatusCodeError(response)
