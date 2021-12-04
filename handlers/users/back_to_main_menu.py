from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data import messages
from keyboards.default import main_menu
from loader import dp, bot
from utils.db_api import db_commands
from states.states import MenuState
from filters import IsPrivate

db = db_commands.DBCommands()


@dp.message_handler(IsPrivate(), Text(equals=["❌Отменить", "❌Bekor qilish"]), state="*")
@dp.message_handler(IsPrivate(), Text(equals=["🏠Bosh menyu", "🏠Главное меню"]), state="*")
async def back_to_menu(message: Message, state: FSMContext):
    user_id = types.User.get_current().id
    await bot.send_chat_action(user_id, "Typing")
    data = await state.get_data()
    lang = data.get("Lang" + str(user_id))
    services = await db.get_all_services(user_id)
    if services:
        active_service = await db.get_active_service(user_id)
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
        await message.answer(messages.main_menu_msg(lang), reply_markup=main_menu(4, lang))
