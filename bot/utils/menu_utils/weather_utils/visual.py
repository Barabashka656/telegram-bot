import datetime

from bot.utils.custom_bot_exceptions import InvalidResponseStatusCodeError
from bot.data.config import VISUAL_API_KEY

import aiohttp


async def get_current_visual_weather(city: str) -> dict | InvalidResponseStatusCodeError:
    content_type = "json"
    language = "ru"
    current_time = str(datetime.datetime.now())
    current_time_in_format = datetime.datetime.fromisoformat(current_time).strftime("%Y-%m-%dT%H:%M:%S")
    unit_group = "metric"
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline" +\
          f"/{city}" +\
          f"/{current_time_in_format}" +\
          f"?maxStations=1&unitGroup={unit_group}" +\
          f"&key={VISUAL_API_KEY}" +\
          f"&contentType={content_type}" +\
          f"&lang={language}" +\
          "&include=current"

    async with aiohttp.ClientSession() as client:
        async with client.get(url=url) as response:
            match response.status:
                case 200:
                    data = await response.json()
                    return data.get('days')[0]
                case _:
                    raise InvalidResponseStatusCodeError(response)
