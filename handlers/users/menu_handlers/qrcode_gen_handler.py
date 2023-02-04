from loader import dp

from keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import menu_newmsg_back_keyboard
from states.menu_states import QrGenState
from utils.menu_utils import generate_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram import types



'''
ЧТО ТАКОЕ QR-КОД:
QR код «QR - Quick Response - Быстрый Отклик» — это двухмерный штрихкод (бар-код), предоставляющий информацию для быстрого ее распознавания с помощью камеры на мобильном телефоне.

При помощи QR-кода можно закодировать любую информацию, например: текст, номер телефона, ссылку на сайт или визитную карточку.
'''

@dp.callback_query_handler(start_menu_callback.filter(category="qr_gen"))
async def set_qr_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer("Введите информацию для кодирования")
    await QrGenState.qr_gen_data.set()



@dp.message_handler(state=QrGenState.qr_gen_data)
async def send_qr(message: types.Message, state: FSMContext):

    file = generate_qrcode(message.text)
    await message.answer_photo(photo = file, reply_markup=menu_newmsg_back_keyboard)
    await state.finish()
