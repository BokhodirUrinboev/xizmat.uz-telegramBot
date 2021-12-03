from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_button = ReplyKeyboardMarkup(
    keyboard=[
     [
        KeyboardButton(text="🇺🇿O'zbek tili"),
        KeyboardButton(text="🇷🇺Русский язык")
     ],

    ],
    resize_keyboard=True
)

