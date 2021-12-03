from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsState(StatesGroup):
    Settings_menu = State()
    Language = State()


class MenuState(StatesGroup):
    no_account_menu = State()
    individual_account_menu = State()
    no_active_menu = State()


class PostsStates(StatesGroup):
    Post_msg_uz = State()
    Post_msg_ru = State()
    Post_forward_uz = State()
    Post_forward_ru = State()
    Post_done = State()
