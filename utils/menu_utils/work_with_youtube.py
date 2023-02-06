from data.config import STORAGE_DIR

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from aiogram import types


def youtube_download(chat_id: str, text: str) -> types.InputFile:
    ydl_opts = {
        'outtmpl': STORAGE_DIR + f"{chat_id}.webm"
        # будет взято из названию на ютубе + .webm или можно задать имя и расширение файла вручную
    }

    try:
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl.download([text])

    except DownloadError:
        ytdl.extract_info(url=f"ytsearch:{text}", download=True)['entries'][0:5]

    return types.InputFile(STORAGE_DIR + f"{chat_id}.webm")
