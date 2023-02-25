from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)


class WeatherState(StatesGroup):
    city_data = State()


class QrScanState(StatesGroup):
    qr_scan_data = State()
