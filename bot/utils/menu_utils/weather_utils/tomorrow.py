from bot.data.config import TOMORROW_IO_API_KEY
from bot.utils.custom_bot_exceptions import InvalidResponseStatusCodeError

import aiohttp


async def get_current_tomorrow_weather(city: str) -> dict | InvalidResponseStatusCodeError:
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={TOMORROW_IO_API_KEY}"

   
    async with aiohttp.ClientSession() as client:
        async with client.get(url=url) as response:
            match response.status:
                case 200:
                    data = await response.json()
                    print(data)
                    print('asfd')
                    return data.get("data").get("values")
                case _:
                    raise InvalidResponseStatusCodeError(response)
