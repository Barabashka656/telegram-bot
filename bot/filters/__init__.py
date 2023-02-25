from .weather_services_filter import (
    IsAccuWeatherFilter,
    IsVisualWeatherFilter,
    IsTomorrowWeatherFilter,
    IsWeatherPremiumFilter,
    IsFirstCurrentWeatherUseFilter,
    IsCurrentCityNotInDatabase
)
from bot.loader import dp

if __name__ == 'filters':
    dp.filters_factory.bind(
        (
            IsAccuWeatherFilter,
            IsVisualWeatherFilter,
            IsTomorrowWeatherFilter,
            IsWeatherPremiumFilter,
            IsFirstCurrentWeatherUseFilter,
            IsCurrentCityNotInDatabase
        ))
