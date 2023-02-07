from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)


class ShortcutGenState(StatesGroup):
    shortcut_gen_data = State()


class ShortcutScanState(StatesGroup):
    shortcut_scan_data = State()
