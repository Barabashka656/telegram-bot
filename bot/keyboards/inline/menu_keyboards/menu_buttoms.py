from bot.data.config import (           # TODO(rename): file
    DISCORD_INVITE_LINK,
    TELEGRAM_LINK
)

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

'''
template
epic_newmsg_cancel_buttom
handMainName_subInfo_sendingFormat_InlineKeyboardType                           #snake_case

handMainName --> epic
subInfo --> newmsg
sendingFormat --> cancel
InlineKeyboardType --> buttom

callback_data   -->
+---------------+------------+
| sendingFormat | menu_level |
+---------------+------------+
| send_message  |     1      |
+---------------+------------+
|   edit_text   |     2      |
+---------------+------------+
|   settings    |     3      |
+---------------+------------+

'''
# message.answer
menu_newmsg_buttom = InlineKeyboardButton(
    text="Назад в меню",
    callback_data="menu:1:menu"
)

# message.edit_text
menu_editmsg_buttom = InlineKeyboardButton(
    text="Назад в меню",
    callback_data="menu:2:menu"
)

# message.answer
epic_cancel_newmsg_buttom = InlineKeyboardButton(
    text="Отказаться от рассылки бесплатных игр",
    callback_data="menu:1:epic_cancel"
)

# message.edit_text
epic_cancel_editmsg_buttom = InlineKeyboardButton(
    text="Отказаться от рассылки бесплатных игр",
    callback_data="menu:2:epic_cancel"
)

# message.answer
epic_resume_editmsg_buttom = InlineKeyboardButton(
    text="Возобновить подписку",
    callback_data="menu:2:epic_yes"
)

# message.answer
epic_sub_newmsg_buttom = InlineKeyboardButton(
    text="Подписаться на рассылку бесплатных игр",
    callback_data="menu:1:epic_yes"
)

# message.edit_text
epic_sub_editmsg_buttom = InlineKeyboardButton(
    text="Подписаться на рассылку бесплатных игр",
    callback_data="menu:2:epic_yes"
)

epic_sub_settings_buttom = InlineKeyboardButton(
    text="Подписаться на рассылку бесплатных игр",
    callback_data="menu:3:epic_yes"
)

epic_cancel_settings_buttom = InlineKeyboardButton(
    text="Отказаться от рассылки бесплатных игр",
    callback_data="menu:3:epic_cancel"
)

# additional buttoms

menu_newmsg_back_keyboard = InlineKeyboardMarkup().insert(menu_newmsg_buttom)
# for qr_scan

menu_editmsg_back_keyboard = InlineKeyboardMarkup().insert(menu_editmsg_buttom)


first_level_menu_keyboard = InlineKeyboardMarkup(row_width=2,
                                                 inline_keyboard=[[
                                                     InlineKeyboardButton(
                                                         text="погода",
                                                         callback_data="menu:1:weather"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="Бесплатные epic игры",
                                                         callback_data="menu:1:epic"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="генерация qr кода",
                                                         callback_data="menu:1:qr_gen"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="сканер qr кода",
                                                         callback_data="menu:1:qr_scan"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="скачать видео с youtube",
                                                         callback_data="menu:1:youtube"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="переводчик",
                                                         callback_data="menu:1:translator"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="ChatGPT (3.5 turbo)",
                                                         callback_data="menu:1:chat_gpt"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="coming soon",
                                                         callback_data="menu:1:soon"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="Генерация сокращённых ссылок",
                                                         callback_data="menu:1:shortcut_gen"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="Расшифровка сокращенных ссылок",
                                                         callback_data="menu:1:shortcut_scan"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="Ресурсы",
                                                         callback_data="menu:1:sources"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="Настройки",
                                                         callback_data="menu:1:settings"
                                                     )
                                                 
                                                 ]])


translator = InlineKeyboardMarkup()


shortcut_sources_keyboard = InlineKeyboardMarkup(row_width=2,
                                                 inline_keyboard=[[
                                                     InlineKeyboardButton(
                                                         text="tinyurl",
                                                         callback_data="menu:1:tinyurl"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="chilpit",
                                                         callback_data="menu:1:chilpit"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="clckru",
                                                         callback_data="menu:1:clckru"
                                                     ),
                                                     InlineKeyboardButton(
                                                         text="dagd",
                                                         callback_data="menu:1:dagd"
                                                     )
                                                 ], [
                                                     InlineKeyboardButton(
                                                         text="isgd",
                                                         callback_data="menu:1:isgd"
                                                     ),
                                                     menu_editmsg_back_keyboard
                                                 ]
                                                 ])


my_sources_keyboard = InlineKeyboardMarkup(row_width=2,
                                           inline_keyboard=[[
                                               InlineKeyboardButton(
                                                   text="Дискорд",
                                                   url=DISCORD_INVITE_LINK
                                               ),
                                               InlineKeyboardButton(
                                                   text="Мой Телеграм",
                                                   url=TELEGRAM_LINK
                                               )
                                           ], [
                                               menu_editmsg_buttom
                                           ]
                                           ])
