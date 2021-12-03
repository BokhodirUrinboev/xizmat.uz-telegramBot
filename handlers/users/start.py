from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from data import messages
from keyboards.default import *
from keyboards.default.lang import language_button
from keyboards.default.menu import main_menu
from loader import dp, bot
from filters import IsPrivate
from states.states import SettingsState, MenuState
from utils.db_api.db_commands import DBCommands

db = DBCommands()


# Command start handler
@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    msg_to_delete = ''
    await bot.send_chat_action(user_id, "Typing")
    await state.reset_state(with_data=False)
    old_user = await db.get_user(user_id)
    if old_user:
        await state.update_data(
            {"Lang"+str(old_user.chat_id): old_user.lang}
        )
        services = await db.get_all_services(user_id)
        if services:
            active_service = await db.get_active_service(old_user.chat_id)
            if active_service:
                if active_service.type == 1:
                    await MenuState.individual_account_menu.set()
                    await message.answer(messages.main_menu_msg(old_user.lang),
                                         reply_markup=main_menu(active_service.type, old_user.lang))
            else:
                await MenuState.no_active_menu.set()
                await message.answer(messages.main_menu_msg(old_user.lang), reply_markup=main_menu(3, old_user.lang))

        else:
            await MenuState.no_account_menu.set()
            await message.answer(messages.main_menu_msg(old_user.lang),
                                                 reply_markup=main_menu(4, old_user.lang))
    else:
        await db.add_new_user()
        await SettingsState.Language.set()
        await message.answer("🌍 Язык/Til:", reply_markup=language_button)
