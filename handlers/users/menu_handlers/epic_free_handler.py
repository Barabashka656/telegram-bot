import datetime

from loader import dp
from utils.db_api.models_peewee import (
    db, EpicFreeGame, EpicMail, Utility
)
from keyboards.inline.menu_keyboards.menu_callback_datas\
    import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import (
    menu_newmsg_buttom, epic_cancel_settings_buttom,
    epic_resume_editmsg_buttom, epic_cancel_newmsg_buttom,
    epic_cancel_editmsg_buttom, epic_sub_newmsg_buttom,
    menu_editmsg_buttom, epic_sub_settings_buttom
)

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.callback_query_handler(start_menu_callback.filter(category="epic"))
async def show_epic_free_games(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    with db:
        games = EpicFreeGame.select()
        x = 0
        for game in games:
            epic_store_keyboard = InlineKeyboardMarkup(row_width=2)
            epic_link = InlineKeyboardButton(text="Открыть Epic games",
                                             url=game.product_slug)

            epic_store_keyboard.insert(epic_link)

            x += 1
            if x == len(games):
                epic_store_keyboard.insert(menu_newmsg_buttom)
                if EpicMail.get_or_none(user_id=call.from_user.id):
                    epic_store_keyboard.insert(epic_cancel_newmsg_buttom)
                else:
                    epic_store_keyboard.insert(epic_sub_newmsg_buttom)
            await call.message.answer_photo(photo=game.key_image_url,
                                            caption=game.description)

            if game.start_date and game.end_date:

                start_date = datetime.datetime.fromisoformat(game.start_date)
                start_date = start_date.strftime("%H:%M %d-%m-%Y")
                end_date = datetime.datetime.fromisoformat(game.end_date)
                end_date = end_date.strftime("%H:%M %d-%m-%Y")

                answer_text = f"{game.title}\n" +\
                              f"Игра бесплатна с {start_date} по {end_date}\n" +\
                              f"<s> {game.original_price}</s> -> Free!"

                await call.message.answer(text=answer_text,
                                          reply_markup=epic_store_keyboard,
                                          parse_mode="html")
            else:
                await call.message.answer(text=f"{game.title} дата неизвестна",
                                          reply_markup=epic_store_keyboard)


@dp.callback_query_handler(start_menu_callback.filter(category="epic_yes"))
async def epic_notif_sub(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    with db:
        raw_notif_date = Utility.get().next_notification
        next_notif_date = datetime.datetime
        next_notif_date = next_notif_date.fromisoformat(raw_notif_date)
        next_notif_date = next_notif_date.strftime("%H:%M %d-%m-%Y")
        EpicMail(
            user_id=call.from_user.id
        ).save()

    answer_text = "Вы подписались на рассылку бесплатных игр\
                   Epic Games Store\n" +\
                  f"Следующая рассылка будет в {next_notif_date}"

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.insert(epic_cancel_editmsg_buttom)
    keyboard.insert(menu_editmsg_buttom)

    menu_level = call.data.split(':')[1]

    if menu_level == "1":
        await call.message.answer(text=answer_text, reply_markup=keyboard)

    elif menu_level == "2":         # TODO: make func keyboards
        my_sources_keyboard = InlineKeyboardMarkup(row_width=1)
        my_sources_keyboard.insert(epic_cancel_editmsg_buttom)
        my_sources_keyboard.insert(menu_editmsg_buttom)
        await call.message.edit_text(text=answer_text,
                                     reply_markup=my_sources_keyboard)
    elif menu_level == "3":             # TODO: settings keyboard
        settings_keyboard = InlineKeyboardMarkup(row_width=1)
        settings_keyboard.insert(epic_cancel_settings_buttom)
        settings_keyboard.insert(menu_editmsg_buttom)
        await call.message.edit_reply_markup(reply_markup=settings_keyboard)


@dp.callback_query_handler(start_menu_callback.filter(category="epic_cancel"))
async def epic_notif_cancel(call: types.CallbackQuery):
    print(datetime.datetime.now())
    await call.answer(cache_time=0)
    with db:
        user = EpicMail.get_or_none(
            user_id=call.from_user.id
        )
        if user:
            user.delete_instance()

    answer_text = "Вы отказались от рассылки бесплатных игр Epic Games Store\n"
    menu_level = call.data.split(':')[1]

    if menu_level == "1":
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.insert(epic_resume_editmsg_buttom)
        keyboard.insert(menu_editmsg_buttom)
        await call.message.answer(text=answer_text, reply_markup=keyboard)
    elif menu_level == "2":
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.insert(epic_resume_editmsg_buttom)
        keyboard.insert(menu_editmsg_buttom)
        await call.message.edit_text(text=answer_text, reply_markup=keyboard)
    elif menu_level == "3":  # TODO: settings keyboard
        settings_keyboard = InlineKeyboardMarkup(row_width=1)
        settings_keyboard.insert(epic_sub_settings_buttom)
        settings_keyboard.insert(menu_editmsg_buttom)
        await call.message.edit_reply_markup(reply_markup=settings_keyboard)
