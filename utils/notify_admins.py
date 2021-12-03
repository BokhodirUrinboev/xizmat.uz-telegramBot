from aiogram import Dispatcher
from data.config import admins
import logging


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Bot Started")
        except Exception as err:
            logging.exception(err)
