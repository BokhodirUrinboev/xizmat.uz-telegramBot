from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from data.config import I18N_DOMAIN, LOCALES_DIR
from utils.db_api.db_commands import DBCommands

db = DBCommands()


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        # getting current user
        user = types.User.get_current()

        if user is None:
            return 'uz'
        # getting language of user from db
        lang = await db.get_language(user.id)

        # if language exists return language
        if lang:
            return lang
        else:
            # if user's language in list of languages  return language
            if user.locale in ['ru', 'uz']:
                return user.locale
            else:
                # otherwise make it Uzbek language by default
                return 'uz'


def setup_middleware(dp):
    # Устанавливаем миддлварь
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n