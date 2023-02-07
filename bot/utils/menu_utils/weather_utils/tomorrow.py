import requests

from data.config import TOMORROW_IO_API_KEY
from custom_bot_exceptions import InvalidResponseStatusCodeError


def current_weather_tomorrow_api(lat: float, lon: float) -> dict | InvalidResponseStatusCodeError:
    url_start = f"https://api.tomorrow.io/v4/timelines?location={str(lat)}%2C%20{str(lon)}&"
    url_end = f"units=metric&timesteps=current&apikey={TOMORROW_IO_API_KEY}"

    data_fields = ["temperature", "temperatureApparent",
                   "dewPoint", "humidity",
                   "windSpeed", "windDirection",
                   "windGust", "pressureSurfaceLevel",
                   "pressureSeaLevel", "cloudCover",
                   "visibility", "cloudBase",
                   "cloudCeiling", "treeIndex",
                   "fireIndex", "snowIntensity",
                   "precipitationType", "uvIndex",
                   "floodIndex", "streamFlow"
                   ]

    for field in data_fields:
        url_start = url_start + "fields=" + field + "&"

    url = url_start + url_end
    response = requests.get(url=url)
    match response:
        case 200:
            return response.json().get("data").get("timelines")[0].get("intervals")[0].get("values")
        case _:
            raise InvalidResponseStatusCodeError(response)
