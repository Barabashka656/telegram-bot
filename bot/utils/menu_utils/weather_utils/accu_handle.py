from .weather_class import AccuWeather


def processing(raw_weather_data: AccuWeather, is_metric: bool) -> str:

    if is_metric:
        weather_data = f"Температура: {raw_weather_data.temperature.metric.value}" +\
                       f"{raw_weather_data.temperature.metric.unit}\n" +\
                       f"Ощущается как {raw_weather_data.apparent_temperature.metric.value}" +\
                       f"{raw_weather_data.apparent_temperature.metric.unit}\n" +\
                       f"Скорость ветра: {raw_weather_data.wind.speed.metric.value} " +\
                       f"{raw_weather_data.wind.speed.metric.unit}\n" +\
                       f"Влажность: {raw_weather_data.humidity} %"
    else:
        weather_data = f"Температура: {raw_weather_data.temperature.imperial.value}" +\
                       f"{raw_weather_data.temperature.imperial.unit}\n" +\
                       f"Ощущается как {raw_weather_data.apparent_temperature.imperial.value}" +\
                       f"{raw_weather_data.apparent_temperature.imperial.unit}\n" +\
                       f"Скорость ветра: {raw_weather_data.wind.speed.imperial.value} " +\
                       f"{raw_weather_data.wind.speed.imperial.unit}\n" +\
                       f"Влажность: {raw_weather_data.humidity} %"
    return weather_data
