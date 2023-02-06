from aiogram.dispatcher.filters.state import StatesGroup, State


class YtDlState(StatesGroup):
    ytdl_data = State()
