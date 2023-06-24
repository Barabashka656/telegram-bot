import io
import os
import logging

from aiogram import types
import qrcode
import cv2
from pyzbar import pyzbar  # https://www.microsoft.com/en-US/download/details.aspx?id=40784 # if error

logger = logging.getLogger(__name__)


def generate_qrcode(data: str) -> types.InputFile:
    buf = io.BytesIO()
    qrcode.make(data).save(buf, format='PNG')
    # You need to seek back to the beginning of the file after writing the initial in memory file...
    buf.seek(0)
    return types.InputFile(buf, "qrcode.png")


def scan_qrcode(filedir: str) -> str:
    img = cv2.imread(filedir)
    barcodes = pyzbar.decode(img)
    os.remove(filedir)
    return barcodes[0].data.decode()
