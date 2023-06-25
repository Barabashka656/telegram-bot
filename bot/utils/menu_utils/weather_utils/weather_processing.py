import logging

from .weather_class import (
    AccuWeather,
    VisualWeather,
    TommorowWeather,
    BaseWeather
)

logger = logging.getLogger(__name__)


def weather_processing_overview(raw_weather_data: BaseWeather) -> str:
    return f"Температура: {raw_weather_data.temperature}\n" +\
           f"Ощущается как {raw_weather_data.apparent_temperature}\n" +\
           f"Скорость ветра: {raw_weather_data.wind_speed} км/ч\n" +\
           f"Давление: {raw_weather_data.pressure} мб\n" +\
           f"Влажность: {raw_weather_data.humidity} %"


def accu_weather_processing(raw_weather_data: AccuWeather) -> str:
    weather_data = raw_weather_data.weather_text + '\n'
    if raw_weather_data.has_precipitation:
        weather_data += raw_weather_data.precipitation_type + "\n"

    return weather_data + f"температура: {raw_weather_data.temperature}\n" +\
                          f"ощущается как: {raw_weather_data.apparent_temperature}\n" +\
                          f"температура в тени\nощущается как: {raw_weather_data.feels_like_shade} \n" +\
                          f"влажность: {raw_weather_data.humidity} %\n" +\
                          f"indoor relative humidity: {raw_weather_data.indoor_relative_humidity}%\n" +\
                          f"{raw_weather_data.pressure_tendency.code}, характер (" +\
                          f"{raw_weather_data.pressure_tendency.localized_text})\n" +\
                          f"{raw_weather_data.pressure} мб\n" +\
                          f"скорость ветра: {raw_weather_data.wind_speed} км/ч\n" +\
                          f"порывы ветра: {raw_weather_data.wind_gust_speed} км/ч\n" +\
                          f"направление: {raw_weather_data.wind_dir}\n" +\
                          f"точка росы: {raw_weather_data.dew_point}\n" +\
                          f"облачность: {raw_weather_data.cloud_cover} %\n" +\
                          f"видимость: {raw_weather_data.visibility} км\n" +\
                          f"кол-во осадков за последний час: {raw_weather_data.precip1hr} мм\n" +\
                          f"уровень уф излучения: {raw_weather_data.uv_index_text}\n" +\
                          f"uv индекс: {raw_weather_data.uv_index}\n"


def tomorrow_weather_processing(raw_weather_data: TommorowWeather) -> str:

    return f"температура: {raw_weather_data.temperature}\n" +\
           f"ощущается как: {raw_weather_data.apparent_temperature}\n" +\
           f"влажность: {raw_weather_data.humidity} %\n" +\
           f"давление: {raw_weather_data.pressure} мб\n" +\
           f"скорость ветра: {raw_weather_data.wind_speed} км/ч\n" +\
           f"порывы ветра: {raw_weather_data.wind_gust_speed} км/ч\n" +\
           f"направление: {raw_weather_data.wind_dir}\n" +\
           f"точка росы: {raw_weather_data.dew_point}\n" +\
           f"облачность: {raw_weather_data.cloud_cover} %\n" +\
           f"видимость: {raw_weather_data.visibility} км\n" +\
           f"uv индекс: {raw_weather_data.uv_index}\n"


def visual_weather_processing(raw_weather_data: VisualWeather) -> str:
    weather_data = raw_weather_data.conditions + '\n'

    return weather_data + f"температура: {raw_weather_data.temperature}\n" +\
                          f"ощущается как: {raw_weather_data.apparent_temperature}\n" +\
                          f"влажность: {raw_weather_data.humidity} %\n" +\
                          f"давление: {raw_weather_data.pressure} мб\n" +\
                          f"скорость ветра: {raw_weather_data.wind_speed} км/ч\n" +\
                          f"порывы ветра: {raw_weather_data.wind_gust_speed} км/ч\n" +\
                          f"направление: {raw_weather_data.wind_dir}\n" +\
                          f"точка росы: {raw_weather_data.dew_point}\n" +\
                          f"облачность: {raw_weather_data.cloud_cover} %\n" +\
                          f"видимость: {raw_weather_data.visibility} км\n" +\
                          f"кол-во осадков за последний час: {raw_weather_data.precip} мм\n" +\
                          f"солнечная энергия: {raw_weather_data.solarenergy} МДж/м²\n" +\
                          f"солнечное излучение: {raw_weather_data.solarradiation} Вт/м²\n" +\
                          f"uv индекс: {raw_weather_data.uv_index}\n"
