from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)


class ChatGptState(StatesGroup):
    chat_gpt_data1 = State()
    chat_gpt_data2 = State()
    chat_gpt_data3 = State()
