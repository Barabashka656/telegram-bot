from bot.loader import dp



 

from bot.loader import dp
from bot.utils.chat_gpt_api import get_openai_response
from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.menu_buttoms\
    import menu_newmsg_back_keyboard
from bot.states.menu_states import ChatGptState

from aiogram.dispatcher.storage import FSMContext
from aiogram import types

INITIAL_DIALOGUE: tuple = (
    {'role': 'system', 'content': 'you are a helpfull ai assistant'},
    
)

@dp.callback_query_handler(start_menu_callback.filter(category="chat_gpt"))
async def set_gpt_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    # await call.message.delete()
    answer_text = "Начинайте диалог\n/stop и кнопка 'назад в меню'\n" +\
                  "для завершения диалога"
    await call.message.answer(text=answer_text,
                              reply_markup=menu_newmsg_back_keyboard)
    await ChatGptState.chat_gpt_data1.set()


@dp.message_handler(state=ChatGptState.chat_gpt_data1)  # TODO(GPT): funcs are the same (DRY) 
async def send_qr(message: types.Message, state: FSMContext):
    user_response = message.text
    if user_response == "/stop":
        return await state.finish()
    previous_message = await message.answer("Подождите немного...")
    messages = list(INITIAL_DIALOGUE)
        
    messages = get_openai_response(user_response, messages)
    async with state.proxy() as data:
        data["messages"] = messages
    answer_text = messages[-1].get('content')
    if answer_text:
        await previous_message.edit_text(text=answer_text,
                                         reply_markup=menu_newmsg_back_keyboard)
        await ChatGptState.chat_gpt_data2.set()
    else:
        answer_text = 'Произошла ошибка (gpt:error 1011)'
        await message.answer(text=answer_text,
                             reply_markup=menu_newmsg_back_keyboard)
        return await state.finish()
    
@dp.message_handler(state=ChatGptState.chat_gpt_data2)
async def send_qr(message: types.Message, state: FSMContext):
    user_response = message.text
    if user_response == "/stop":
        return await state.finish()
    previous_message = await message.answer("Подождите немного...")
    messages = await state.get_data("messages")
    messages = get_openai_response(user_response, messages)
    async with state.proxy() as data:
        data["messages"] = messages
    answer_text = messages[-1].get('content')
    if answer_text:
        await previous_message.edit_text(text=answer_text,
                                   reply_markup=menu_newmsg_back_keyboard)
        await ChatGptState.chat_gpt_data3.set()
    else:
        answer_text = 'Произошла ошибка (gpt:error 1011)'
        await message.answer(text=answer_text,
                                   reply_markup=menu_newmsg_back_keyboard)
        return await state.finish()

@dp.message_handler(state=ChatGptState.chat_gpt_data3)
async def send_qr(message: types.Message, state: FSMContext):
    user_response = message.text
    if user_response == "/stop":
        return await state.finish()
    await message.answer("Подождите немного...")
    messages = await state.get_data("messages")
    previous_message = messages = get_openai_response(user_response, messages)
    async with state.proxy() as data:
        data["messages"] = messages
    answer_text = messages[-1].get('content')
    if answer_text:
        await previous_message.edit_text(text=answer_text,
                                   reply_markup=menu_newmsg_back_keyboard)
        await ChatGptState.chat_gpt_data2.set()
    else:
        answer_text = 'Произошла ошибка (gpt:error 1011)'
        await message.answer(text=answer_text,
                                   reply_markup=menu_newmsg_back_keyboard)
        return await state.finish()