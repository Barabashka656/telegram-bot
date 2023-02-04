from data.config import STORAGE_DIR
from loader import dp

from keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import menu_editmsg_qrScanState_buttom, menu_editmsg_back_keyboard,\
                                              menu_newmsg_back_keyboard
from states.menu_states import QrScanState
from utils.menu_utils import scan_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram import types

'''
ЧТО ТАКОЕ QR-КОД:
QR код «QR - Quick Response - Быстрый Отклик» — это двухмерный штрихкод (бар-код), предоставляющий информацию для быстрого ее распознавания с помощью камеры на мобильном телефоне.

При помощи QR-кода можно закодировать любую информацию, например: текст, номер телефона, ссылку на сайт или визитную карточку.
'''

@dp.callback_query_handler(start_menu_callback.filter(category="qr_scan"))
async def set_qr_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer("Отправьте qr код")
    await QrScanState.qr_scan_data.set()

@dp.message_handler(state=QrScanState.qr_scan_data)
async def send_qr_data(message: types.Message): #, state: FSMContext):
    keyboard = InlineKeyboardMarkup().insert(menu_editmsg_qrScanState_buttom)
    await message.answer(text = "Отправьте не текст, а фото", reply_markup=keyboard)

@dp.message_handler(state=QrScanState.qr_scan_data, content_types=types.ContentTypes.PHOTO)
async def send_qr_data(message: types.Message, state: FSMContext):
    filedir = STORAGE_DIR + f"{message.from_user.id}.png"
    await message.photo[-1].download(destination_file = filedir)
    text = scan_qrcode(filedir)
    await message.answer(text = text, reply_markup=menu_newmsg_back_keyboard)
    await state.finish()

