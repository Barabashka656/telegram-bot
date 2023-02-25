from .menu_buttoms import menu_editmsg_buttom

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

first_level_weather_keyboard = InlineKeyboardMarkup(row_width=2,
                                                    inline_keyboard=[[
                                                        InlineKeyboardButton(
                                                            text="погода сейчас",
                                                            callback_data="menu:2:current_weather"
                                                        ),
                                                        InlineKeyboardButton(
                                                            text="прогноз погоды (soon)",
                                                            callback_data="menu:2:weather_forecast"
                                                        )
                                                    ], [
                                                        menu_editmsg_buttom
                                                    ]])

current_weather_editmsg_back_buttom = InlineKeyboardButton(
    text="Назад",
    callback_data="menu:1:current_weather_back"
)

current_weather_choose_service_keyboard = InlineKeyboardMarkup(row_width=3,
                                                               inline_keyboard=[[
                                                                   InlineKeyboardButton(
                                                                       text="AccuWeather",
                                                                       callback_data="menu:3:current_accu_setup"
                                                                   ),
                                                                   InlineKeyboardButton(
                                                                       text="Visual Weather",
                                                                       callback_data="menu:3:current_visual_setup"
                                                                   ),
                                                                   InlineKeyboardButton(
                                                                       text="Tomorrow.io",
                                                                       callback_data="menu:3:current_tomorrow_setup"
                                                                   )
                                                               ], [
                                                                   current_weather_editmsg_back_buttom
                                                               ]])


def accu_weather_keyboard(weather_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().insert(
        InlineKeyboardButton(
            text="посмотреть на сайте",
            url=weather_link
        )
    )
