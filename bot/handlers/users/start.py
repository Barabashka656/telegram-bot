from bot.loader import dp
from bot.keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from bot.keyboards.inline.menu_keyboards.menu_buttoms import first_level_menu_keyboard
from bot.utils.db_api.models_peewee import (
    db,
    User
)
from bot.states.menu_states import QrScanState


from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types


@dp.message_handler(CommandStart())
async def bot_start_new(message: types.Message):
    answer_text = f"Привет, {message.from_user.full_name}!\nЧто я умею:"
    await message.answer(text=answer_text, reply_markup=first_level_menu_keyboard)
    with db:
        if not User.get_or_none(user_id=message.from_user.id):
            User(user_id=message.from_user.id,
                 first_name=message.from_user.full_name,
                 username=message.from_user.username
                 ).save()


@dp.callback_query_handler(start_menu_callback.filter(category="menu", menu_level="1"))
async def bot_start(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.answer(text="Выбирай категорию!", reply_markup=first_level_menu_keyboard)


@dp.callback_query_handler(start_menu_callback.filter(category="menu", menu_level="2"))
async def bot_start_edit(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.edit_text(text="Выбирай категорию!", reply_markup=first_level_menu_keyboard)


@dp.callback_query_handler(start_menu_callback.filter(category="menu_qrScanState", menu_level="2"),
                           state=QrScanState.qr_scan_data)
async def bot_start_qr_state(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    await state.finish()
    await call.message.edit_text(text="Выбирай категорию!", reply_markup=first_level_menu_keyboard)
