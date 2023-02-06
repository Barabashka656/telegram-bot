from loader import dp

from keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import (
    shortcut_sources_keyboard,
    menu_newmsg_back_keyboard,
    menu_editmsg_back_keyboard
)
from states.menu_states import ShortcutGenState
from utils.menu_utils import shortcut_apies
from utils.db_api.models_peewee import (
    db,
    ShortcutTable
)

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="shortcut_gen"))
async def set_shortcut_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    with db:
        shortcut_source_from_db = ShortcutTable.get_or_none(
            user_id=call.from_user.id
        )
        if not shortcut_source_from_db:
            answer_text = "Похоже, вы еще не выбрали сервис для\
                          сокращения ссылок, выберете один ниже"
            await call.message.edit_text(text=answer_text,
                                         reply_markup=shortcut_sources_keyboard)
        else:
            await call.message.edit_text("Введите ссылку, которую требуется сократить")
            await ShortcutGenState.shortcut_gen_data.set()


@dp.message_handler(state=ShortcutGenState.shortcut_gen_data)
async def send_shortcut_url(message: types.Message, state: FSMContext):
    await message.delete()

    with db:
        source = ShortcutTable.get(user_id=message.from_user.id).shortcut_source

    shortcut_func = getattr(shortcut_apies, source)
    shortcut_url = shortcut_func(message.text, True)
    if shortcut_url[0]:
        print(shortcut_url)
        answer_text = "я не могу сократить данную ссылку("
        await message.answer(text=answer_text, reply_markup=menu_editmsg_back_keyboard)
        await state.finish()
    else:
        answer_text = f"<code>{message.text}</code>\n\
                                \n------------------------>\
                                    \n\n<code>{shortcut_url[1]}</code>"
        await message.answer(text=answer_text, reply_markup=menu_newmsg_back_keyboard)
        await state.finish()


@dp.callback_query_handler(start_menu_callback.filter(category=shortcut_apies.shortcut_services))
async def set_shortcut_service_in_db(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    try:
        source = call.data.split(':')[2]
        with db:
            ShortcutTable(
                user_id=call.from_user.id,
                shortcut_source=source
            ).save()
            answer_text = f"Вы выбрали сервис для сокращения ссылок {source}\
                                                \nВведите ссылку, которую требуется сократить"
            await call.message.edit_text(text=answer_text)
            await ShortcutGenState.shortcut_gen_data.set()
    except Exception as e:
        print(e.args)
        await call.message.answer(text="Произошла ошибка")
        await call.message.answer(text="Выбирай категорию(", reply_markup=menu_newmsg_back_keyboard)
