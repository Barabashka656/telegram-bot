from bot.loader import dp
from bot.utils.chat_gpt_api import get_openai_response

from aiogram import types


@dp.message_handler()
async def other_messages_handler(message: types.Message):
    wait_msg = await message.answer("Подождите немного...")
    await wait_msg.edit_text(text=get_openai_response(message.text))
