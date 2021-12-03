from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
# from . import language_middleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())