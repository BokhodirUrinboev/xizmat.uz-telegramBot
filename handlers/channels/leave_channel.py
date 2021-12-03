from aiogram import types

from data.config import GROUP_ID
from loader import dp, bot


# for security measures if bot added to any channel it will leave the channel
@dp.channel_post_handler(content_types=types.ContentType.ANY)
async def bot_echo(message: types.Message):
    try:
        await bot.send_message(GROUP_ID, str(message.chat.as_json())+"bot in channel")
        await message.answer('You can\'t add me to this chat you have no right to do this')
        await bot.leave_chat(message.chat.id)
    except Exception as e:
        await bot.send_message(GROUP_ID, str(e))
        await bot.leave_chat(message.chat.id)
        await bot.send_message(GROUP_ID, str(message.chat.as_json()) + "bot removed himself from channel")
        return
    await bot.send_message(GROUP_ID, str(message.chat.as_json()) + "bot removed himself from channel")
