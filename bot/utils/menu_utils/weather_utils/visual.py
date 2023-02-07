from pprint import pprint
import datetime

from custom_bot_exceptions import InvalidResponseStatusCodeError
from data.config import VISUAL_API_KEY
import requests


def get_current_weather(city: str) -> dict | InvalidResponseStatusCodeError:
    content_type = "json"
    language = "ru"
    current_time = str(datetime.datetime.now())
    current_time_in_format = datetime.datetime.fromisoformat(current_time).strftime("%Y-%m-%dT%H:%M:%S")
    unit_group = "metric"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline\
        /{city}\
        /{current_time_in_format}\
        ?maxStations=1&unitGroup={unit_group}\
        &key={VISUAL_API_KEY}\
        &contentType={content_type}\
        &lang={language}\
        &include=current"

    response = requests.get(url=url)
    match response:
        case 200:
            return response.json()[0]
        case _:
            raise InvalidResponseStatusCodeError(response)
