from pprint import pprint
import random
import string

from geopy import geocoders
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim


def create_random_user_asgent(min_length: int, max_length: int) -> str:
    '''function that generates a random string from min_length to max_length'''

    return ''.join(random.sample(string.ascii_lowercase, k=random.randint(min_length, max_length)))


async def get_cords_by_city_name_async(name: str):   # TODO(aiohttp): remake func using aiohttp
    random_user_agent = create_random_user_asgent(7, 13)

    async with Nominatim(
        user_agent=random_user_agent,
        adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(name)
        print(location.address)
        print(location.latitude)
        print(location.longitude)
        await (location.latitude, location.longitude)


def get_cords_by_city_name_sync(city: str) -> tuple:
    random_user_agent = ''.join(random.sample(string.ascii_lowercase, k=random.randint(7, 13)))
    geolocator = geocoders.Nominatim(user_agent=random_user_agent)
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude)
