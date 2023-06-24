from bot.data.config import STORAGE_PATH
from bot.loader import dp

from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback

from bot.keyboards.inline.menu_keyboards.menu_buttoms import (
    menu_editmsg_back_keyboard,
    menu_newmsg_back_keyboard
)
from bot.states.menu_states import QrScanState
from bot.utils.menu_utils.work_with_qr import scan_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="qr_scan"))
async def set_qr_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer("Отправьте qr код")
    await QrScanState.qr_scan_data.set()


@dp.message_handler(state=QrScanState.qr_scan_data)
async def handle_wrong_update(message: types.Message):  # TODO(rename): rename func
    answer_text = "Отправьте не текст, а фото"
    await message.answer(text=answer_text, reply_markup=menu_editmsg_back_keyboard)


@dp.message_handler(state=QrScanState.qr_scan_data,
                    content_types=types.ContentTypes.PHOTO)
async def get_qr(message: types.Message, state: FSMContext):
    filedir = STORAGE_PATH + f"{message.from_user.id}.png"
    await message.photo[-1].download(destination_file=filedir)
    answer_text = scan_qrcode(filedir)
    await message.answer(text=answer_text, reply_markup=menu_newmsg_back_keyboard)
    await state.finish()
