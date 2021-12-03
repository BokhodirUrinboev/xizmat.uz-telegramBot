from loader import _
import datetime
import re


def choose_lang_msg():
    msg = "Выберите язык➡️\n Tilni tanlang➡️"
    return msg


def main_menu_msg(lang):
    msg = _("📍Siz bosh menyudasiz", locale=lang)
    return msg


def settings_menu_msg():
    msg = _("🔍O'zgartirmoqchi bo'lgan sozlamani tanlang")
    return msg


def change_lang_msg():
    msg = _("Tillardan birini tanlang👇")
    return msg
