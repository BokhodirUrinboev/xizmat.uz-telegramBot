from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def settings_menu_btn():
    language_change_key = KeyboardButton(text=_("🌏Tilni o'zgartirish"))
    back_to_menu_key = KeyboardButton(text=_("🏠Bosh menyu"))

    menu_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                language_change_key
            ],
            [
                back_to_menu_key
            ]
        ], resize_keyboard=True
    )
    return menu_button


def language_change_btn():
    uzb_lang = KeyboardButton(text="🇺🇿O'zbek tili")
    rus_lang = KeyboardButton(text="🇷🇺Русский язык")
    eng_lang = KeyboardButton(text="🇬🇧  English")
    back_key = KeyboardButton(text=_("⬅️Ortga"))
    back_to_menu_key = KeyboardButton(text=_("🏠Bosh menyu"))
    language_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                uzb_lang
            ],
            [
                rus_lang
            ],
            [
                back_key,
                back_to_menu_key
            ]



        ],
        resize_keyboard=True
    )
    return language_button
