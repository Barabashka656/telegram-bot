import os

from bot.data.config import STORAGE_DIR
from bot.loader import bot, dp
from bot.utils.db_api.models_peewee import (
    db,
    YoutubeDlInfo
)
from bot.utils.menu_utils import youtube_download
from bot.keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from bot.keyboards.inline.menu_keyboards.menu_buttoms import (
    menu_newmsg_back_keyboard,
    menu_editmsg_back_keyboard
)
from bot.states.menu_states import YtDlState

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="youtube"))
async def set_yt_dlp_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer(text="Введите ссылку на ютуб видео, которое надо скачать",
                              reply_markup=menu_editmsg_back_keyboard)
    await YtDlState.ytdl_data.set()


@dp.message_handler(state=YtDlState.ytdl_data)
async def send_yt_video(message: types.Message, state: FSMContext):

    with db:
        yt = YoutubeDlInfo.get_or_none(user_id=message.from_user.id, yt_url=message.text)
        if yt:
            await message.answer_video(video=yt.file_id, caption='Не повторяйся!',
                                       reply_markup=menu_newmsg_back_keyboard)
            await state.finish()
            return

    file_dir = STORAGE_DIR + f"{message.from_user.id}.webm"
    message_tobe_removed = await bot.send_message(message.chat.id, 'скачиваем видео')

    youtube_video = youtube_download(chat_id=message.from_user.id, text=message.text)
    # TODO(error) handle telegram limit error
    await message_tobe_removed.edit_text(text="отправляем видео")
    video_id = await message.answer_video(video=youtube_video, reply_markup=menu_newmsg_back_keyboard)

    YoutubeDlInfo(user_id=message.from_user.id,
                  yt_url=message.text,
                  file_id=video_id.video.file_id
                  ).save()

    await message_tobe_removed.delete()
    os.remove(file_dir)
    await state.finish()
