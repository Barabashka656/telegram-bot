import logging

from .weather_services_filter import (
    IsAccuWeatherFilter,
    IsVisualWeatherFilter,
    IsTomorrowWeatherFilter,
    IsWeatherPremiumFilter,
    IsFirstCurrentWeatherUseFilter,
    IsCurrentCityNotInDatabase
)
from bot.loader import dp

logger = logging.getLogger(__name__)


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
