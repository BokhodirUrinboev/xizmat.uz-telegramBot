from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from data import messages
from keyboards.default import settings_menu_btn, language_change_btn
from loader import dp
from utils.db_api import db_commands
from states.states import SettingsState, MenuState
from filters import IsPrivate

db = db_commands.DBCommands()


@dp.message_handler(IsPrivate(), Text(equals=["⬅️Назад", "⬅️Ortga"]), state=SettingsState.Language)
@dp.message_handler(IsPrivate(), Text(equals=["⚙️Sozlamalar", "⚙️Настройки"]),  state=MenuState.no_account_menu)
@dp.message_handler(IsPrivate(), Text(equals=["⚙️Sozlamalar", "⚙️Настройки"]),  state=MenuState.individual_account_menu)
@dp.message_handler(IsPrivate(), Text(equals=["⚙️Sozlamalar", "⚙️Настройки"]),  state=MenuState.no_active_menu)
async def setting_menu(message: Message, state: FSMContext):
    await message.answer(messages.settings_menu_msg(), reply_markup=settings_menu_btn())
    await SettingsState.Settings_menu.set()


@dp.message_handler(IsPrivate(), Text(equals=["🌏Tilni o'zgartirish", "🌏Изменить язык"]), state=SettingsState.Settings_menu)
async def change_lang(message: Message, state: FSMContext):
    await SettingsState.Language.set()
    await message.answer(messages.change_lang_msg(), reply_markup=language_change_btn())
