from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, _
from filters import IsPrivate


@dp.message_handler(IsPrivate(), content_types=[types.ContentType.ANY], state='*')
async def unknown_message_handler(message: types.Message, state: FSMContext):
    await message.reply(_("❗️Siz noto'g'ri buyruqni kiritdingiz"))
