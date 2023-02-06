import os

from data.config import STORAGE_DIR
from loader import bot, dp
from utils.db_api.models_peewee import (
    db,
    YoutubeDlInfo
)
from utils.menu_utils import youtube_download
from keyboards.inline.menu_keyboards.menu_callback_datas import start_menu_callback
from keyboards.inline.menu_keyboards.menu_buttoms import menu_newmsg_back_keyboard
from states.menu_states import YtDlState

from aiogram.dispatcher.storage import FSMContext
from aiogram import types


@dp.callback_query_handler(start_menu_callback.filter(category="youtube"))
async def set_yt_dlp_state(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    await call.message.delete()
    await call.message.answer(text="Введите ссылку на ютуб видео, которое надо скачать")
    await YtDlState.ytdl_data.set()


@dp.message_handler(state=YtDlState.ytdl_data)
async def send_video(message: types.Message, state: FSMContext):

    with db:
        yt = YoutubeDlInfo.get_or_none(user_id=message.from_user.id, yt_url=message.text)
        if yt:
            await message.answer_video(video=yt.file_id, caption='Не повторяйся!',
                                       reply_markup=menu_newmsg_back_keyboard)
            await state.finish()
            return

    file_dir = STORAGE_DIR + f"{message.from_user.id}.webm"
    m = await bot.send_message(message.chat.id, 'скачиваем видео')

    file = youtube_download(chat_id=message.from_user.id, text=message.text)
    # TODO handle telegram limit error
    await m.edit_text(text="отправляем видео")
    Message = await message.answer_video(video=file, reply_markup=menu_newmsg_back_keyboard)

    YoutubeDlInfo(user_id=message.from_user.id,
                  yt_url=message.text,
                  file_id=Message.video.file_id
                  ).save()

    await m.delete()
    os.remove(file_dir)
    await state.finish()
