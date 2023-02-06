import io
import os

from aiogram import types
import qrcode
import cv2
from pyzbar import pyzbar  # https://www.microsoft.com/en-US/download/details.aspx?id=40784 # if error


def generate_qrcode(data: str) -> types.InputFile:
    buf = io.BytesIO()
    qrcode.make(data).save(buf, format='PNG')
    buf.seek(0)  # You need to seek back to the beginning of the file after writing the initial in memory file...
    return types.InputFile(buf, "qrcode.png")


def scan_qrcode(filedir: str) -> str:
    img = cv2.imread(filedir)
    barcodes = pyzbar.decode(img)
    os.remove(filedir)
    return barcodes[0].data.decode()

# TODO: advanced qr //pip qrcode
