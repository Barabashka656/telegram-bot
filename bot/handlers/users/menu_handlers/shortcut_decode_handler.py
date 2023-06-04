import re

from bot.loader import dp

from bot.keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from bot.keyboards.inline.menu_keyboards.menu_buttoms import (
    menu_editmsg_back_keyboard,
    menu_newmsg_back_keyboard
)
from bot.states.menu_states import ShortcutScanState
from bot.utils.menu_utils import shortcut_apies

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(
    category="shortcut_scan"))
async def set_shortcut_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    answer_text = "Введите ссылку, которую требуется расшифровать"
    await call.message.edit_text(text=answer_text)
    await ShortcutScanState.shortcut_scan_data.set()


@dp.message_handler(state=ShortcutScanState.shortcut_scan_data)
async def send_shortcut_url(message: types.Message, state: FSMContext):
    await message.delete()
    url = re.search("(?P<url>https?://[^\s]+)", message.text)
    if url:
        url = url.group()
    else:
        answer_text = "я не могу найти ссылку в вашем сообщении"
        await message.answer(text=answer_text, reply_markup=menu_editmsg_back_keyboard)
        await state.finish()
        return
    error = False
    shortcut_decode = shortcut_apies.shortcut_services[0:1]
    try:
        shortcut_func = getattr(shortcut_apies, shortcut_decode[0])
        shortcut_url = shortcut_func(message.text, False)
    except Exception as e:
        print("short_scan_err", e.args)
        print(e)
        try:
            shortcut_func = getattr(shortcut_apies, shortcut_decode[1])
            shortcut_url = shortcut_func(message.text, False)
        except Exception as e:
            print("short_scan_err2", e.args)
            print(e)
            print(shortcut_url)
            error = True
            answer_text = "я не могу расшифровать данную ссылку("
            await message.answer(text=answer_text,
                                 reply_markup=menu_editmsg_back_keyboard)
            await state.finish()

    if not error:
        if message.text == shortcut_url[1]:
            answer_text = 'данная ссылка не была сокращенной'
        else:
            answer_text = f"<code>{message.text}</code>\n\
                                    \n------------------------>\
                                        \n\n<code>{shortcut_url[1]}</code>"
        await message.answer(text=answer_text, reply_markup=menu_newmsg_back_keyboard, parse_mode='HTML')
        await state.finish()
