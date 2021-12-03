from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def main_menu(service_type, lang):
    # individual =1
    # business = 2
    # no active service = 3
    # no services at all = 4
    balance_btn = KeyboardButton(text=_("💰Balans", locale=lang))
    add_account_btn = KeyboardButton(text=_("➕Akkaunt qo'shish", locale=lang))
    accounts_btn = KeyboardButton(text=_("🔐Akkauntlar", locale=lang))
    help_btn = KeyboardButton(text=_("❓Yordam", locale=lang))
    settings_btn = KeyboardButton(text=_("⚙️Sozlamalar", locale=lang))
    services_btn = KeyboardButton(text=_("🧰Xizmatlar", locale=lang))
    if service_type == 1:
        individual_menu_button = ReplyKeyboardMarkup(
            keyboard=[
                [
                    services_btn,
                    balance_btn
                ],
                [
                    accounts_btn,
                    help_btn,
                    settings_btn
                ],
            ], resize_keyboard=True
        )
        return individual_menu_button

    elif service_type == 2:
        business_menu_button = ReplyKeyboardMarkup(
            keyboard=[
                [
                    services_btn,
                    balance_btn
                ],
                [
                    accounts_btn,
                    help_btn,
                    settings_btn
                ],
            ], resize_keyboard=True
        )
        return business_menu_button
    elif service_type == 3:
        no_active_service = ReplyKeyboardMarkup(
            keyboard=[
                [
                    accounts_btn
                ],
                [
                    help_btn,
                    settings_btn,
                ]
            ], resize_keyboard=True
        )
        return no_active_service
    elif service_type == 4:
        no_services = ReplyKeyboardMarkup(
            keyboard=[
                [
                    add_account_btn
                ],
                [
                    help_btn,
                    settings_btn,
                ]
            ], resize_keyboard=True
        )
        return no_services
