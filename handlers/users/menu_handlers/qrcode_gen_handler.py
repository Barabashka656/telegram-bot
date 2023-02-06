from loader import dp

from keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms\
    import menu_newmsg_back_keyboard
from states.menu_states import QrGenState
from utils.menu_utils import generate_qrcode

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="qr_gen"))
async def set_qr_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer("Введите информацию для кодирования")
    await QrGenState.qr_gen_data.set()


@dp.message_handler(state=QrGenState.qr_gen_data)
async def send_qr(message: types.Message, state: FSMContext):

    qr_code_photo = generate_qrcode(message.text)
    await message.answer_photo(photo=qr_code_photo,
                               reply_markup=menu_newmsg_back_keyboard)
    await state.finish()
