from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def cancel_button():
    cancel_btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("❌Bekor qilish"))
            ]
        ], resize_keyboard=True
    )
    return cancel_btn


def back_button(lang, btn_type):
    back_key = KeyboardButton(text=_("⬅️Ortga", locale=lang))
    back_to_menu_key = KeyboardButton(text=_("🏠Bosh menyu", locale=lang))
    add_account_key = KeyboardButton(text=_("➕Akkaunt qo'shish", locale=lang))
    remove_account_key = KeyboardButton(text=_("🗑Akkaunt o'chirish", locale=lang))
    if btn_type == 0:
        back = ReplyKeyboardMarkup(
            keyboard=[
                [
                    back_key
                ]
            ], resize_keyboard=True
        )
        return back
    elif btn_type == 1:
        back = ReplyKeyboardMarkup(
            keyboard=[
                [
                    back_key

                ],
                [
                    back_to_menu_key

                ]
            ], resize_keyboard=True
        )
        return back
    elif btn_type == 2:
        back = ReplyKeyboardMarkup(
            keyboard=[
                [
                    back_to_menu_key
                ]
            ], resize_keyboard=True
        )
        return back
    elif btn_type == 3:
        back = ReplyKeyboardMarkup(
            keyboard=[
                [
                    add_account_key

                ],
                [
                    remove_account_key
                ],
                [
                    back_to_menu_key
                ],
            ], resize_keyboard=True
        )
        return back

