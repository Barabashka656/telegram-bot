from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)


class QrGenState(StatesGroup):
    qr_gen_data = State()


class QrScanState(StatesGroup):
    qr_scan_data = State()
