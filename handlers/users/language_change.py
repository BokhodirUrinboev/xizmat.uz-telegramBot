from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data import messages
from keyboards.default.menu import main_menu
from loader import dp, bot
from utils.db_api import db_commands
from states.states import SettingsState, MenuState
from filters import IsPrivate
db = db_commands.DBCommands()


@dp.message_handler(IsPrivate(), Text(equals=["🇺🇿O'zbek tili","🇷🇺Русский язык"]),  state=SettingsState.Language)
async def change_lang(message: Message, state: FSMContext):
    user_id = types.User.get_current().id
    await bot.send_chat_action(user_id, "Typing")
    lang = []
    old_user = await db.get_user(user_id)
    if message.text == "🇷🇺Русский язык":
        await db.set_language(user_id, 'ru')
        lang = 'ru'
        await state.update_data(
            {"Lang" + str(user_id): 'ru'}
        )
    elif message.text == "🇺🇿O'zbek tili":
        await db.set_language(user_id, 'uz')
        lang = 'uz'
        await state.update_data(
            {"Lang" + str(user_id): 'uz'}
        )
    elif message.text == "🇬🇧  English":
        await db.set_language(user_id, 'en')
        lang = 'en'
        await state.update_data(
            {"Lang" + str(user_id): 'en'}
        )

    services = await db.get_all_services(user_id)
    if services:
        active_service = await db.get_active_service(old_user.chat_id)
        if active_service:
            if active_service.type == 1:
                await MenuState.individual_account_menu.set()
                await message.answer(messages.main_menu_msg(lang),
                                     reply_markup=main_menu(active_service.type, lang))
        else:
            await MenuState.no_active_menu.set()
            await message.answer(messages.main_menu_msg(lang), reply_markup=main_menu(3, lang))

    else:
        await MenuState.no_account_menu.set()
        await message.answer(messages.main_menu_msg(lang),
                                             reply_markup=main_menu(4, lang))

