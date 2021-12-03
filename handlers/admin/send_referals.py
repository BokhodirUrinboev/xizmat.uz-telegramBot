import asyncio
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions
from states.states import PostsStates
from data.config import admins
from filters import IsPrivate
from aiogram.types import ReplyKeyboardMarkup
from loader import dp, bot
from utils.db_api import db_commands
db = db_commands.DBCommands()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


# custom  send message for broadcasting method with keyboard
async def send_message_with_keyboard(user_id: int, text: str, keyboard: ReplyKeyboardMarkup(), disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification, reply_markup=keyboard)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


# custom method for sanding posts for broadcast
async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


# custom method for sanding forwarded posts for broadcast
async def forward_message(user_id: int, from_chat_id: int, msg_id: int, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.forward_message(user_id, from_chat_id=from_chat_id, message_id=msg_id, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await forward_message(user_id, from_chat_id, msg_id)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


# broadcast method for forwarded posts
async def broadcaster_forward(from_chat_id, msg_id_uz, msg_id_ru) -> int:
    """
    Simple broadcaster For forwarded messages
    :return: Count of messages
    """
    all_users = await db.get_all_users()
    count_all = 0
    try:
        for user in all_users:
            if user.lang == 'uz' and user.lang is not None:
                if await forward_message(user.chat_id, from_chat_id, msg_id_uz):
                    count_all += 1
                await asyncio.sleep(.05)
                # 20 messages per second (Limit: 30 messages per second)
            elif user.lang == 'ru' and user.lang is not None:
                if await forward_message(user.chat_id, from_chat_id, msg_id_ru):
                    count_all += 1
                await asyncio.sleep(.05)
                # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count_all} messages successful sent.")

    return count_all


# broadcast method for posts
async def broadcaster_text(msg_uz, msg_ru) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    all_users = await db.get_all_users()
    count_all = 0
    try:
        for user in all_users:
            if user.lang == 'uz':
                if await send_message(user.chat_id, msg_uz):
                    count_all += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
            elif user.lang == 'ru':
                if await send_message(user.chat_id, msg_ru):
                    count_all += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)

    finally:
        log.info(f"{count_all} messages successful sent.")

    return count_all


# create post
@dp.message_handler(IsPrivate(), text="!addPost", user_id=admins, state='*')
async def add_new_post(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    await bot.send_message(user_id, "Enter post in uzbek")
    await PostsStates.Post_msg_uz.set()


# save uzbek post
@dp.message_handler(IsPrivate(), content_types=[types.ContentType.TEXT], user_id=admins, state=PostsStates.Post_msg_uz)
async def add_new_post_text_uz(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    await state.update_data(
        {"Post_uz" + str(user_id): message.text}
    )
    await bot.send_message(user_id, "Enter post in russian")
    await PostsStates.Post_msg_ru.set()


# save russian post
@dp.message_handler(IsPrivate(), content_types=[types.ContentType.TEXT], user_id=admins, state=PostsStates.Post_msg_ru)
async def add_new_post_text_ru(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    await state.update_data(
        {"Post_ru" + str(user_id): message.text}
    )
    await bot.send_message(user_id, "Done ✅")
    await PostsStates.Post_done.set()


# show posts in both language
@dp.message_handler(IsPrivate(), text="!showPost", user_id=admins, state='*')
async def show_post(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    data = await state.get_data()
    post_ru = data.get("Post_ru" + str(user_id))
    post_uz = data.get("Post_uz" + str(user_id))
    if post_uz:
        await bot.send_message(user_id, post_uz)
    if post_ru:
        await bot.send_message(user_id, post_ru)


# save forwarded uzbek post
@dp.message_handler(IsPrivate(), content_types=[types.ContentType.ANY], user_id=admins, state=PostsStates.Post_forward_uz)
async def add_new_forwarded_post_data_uz(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    from_chat_id = user_id
    msg_id = message.message_id
    await state.update_data(
        {
            "Forward_from" + str(user_id): from_chat_id,
            "Forward_msg_id_uz" + str(user_id): msg_id
         }
    )
    await bot.send_message(user_id, "Done ✅")
    await PostsStates.Post_done.set()


# save forwarded russian post
@dp.message_handler(IsPrivate(), content_types=[types.ContentType.ANY], user_id=admins, state=PostsStates.Post_forward_ru)
async def add_new_forwarded_post_data_uz(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    from_chat_id = user_id
    msg_id = message.message_id
    await state.update_data(
        {
            "Forward_from" + str(user_id): from_chat_id,
            "Forward_msg_id_ru" + str(user_id): msg_id
         }
    )
    await bot.send_message(user_id, "Done ✅")
    await PostsStates.Post_done.set()


# show forwarded uzbek post
@dp.message_handler(IsPrivate(), text="!showForward_uz", user_id=admins, state='*')
async def show_forward_uz(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    data = await state.get_data()
    from_chat_id = data.get("Forward_from" + str(user_id))
    msg_id = data.get("Forward_msg_id_uz" + str(user_id))
    if from_chat_id and msg_id:
        await bot.forward_message(user_id, from_chat_id, msg_id)


# show forward ed russian post
@dp.message_handler(IsPrivate(), text="!showForward_ru", user_id=admins, state='*')
async def show_forward_ru(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    data = await state.get_data()
    from_chat_id = data.get("Forward_from" + str(user_id))
    msg_id = data.get("Forward_msg_id_ru" + str(user_id))
    if from_chat_id and msg_id:
        await bot.forward_message(user_id, from_chat_id, msg_id)


# start forwarding uzbek posts
@dp.message_handler(IsPrivate(), text="!forwardPost_uz", user_id=admins, state='*')
async def add_new_forwarded_post_uz(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    await bot.send_message(user_id, "now forward the message in Uzbek !!!")
    await PostsStates.Post_forward_uz.set()


# start forwarding russian posts
@dp.message_handler(IsPrivate(), text="!forwardPost_ru", user_id=admins, state='*')
async def add_new_forwarded_post_ru(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    await bot.send_message(user_id, "now forward the message in Russian !!!")
    await PostsStates.Post_forward_ru.set()


# command for publishing post
@dp.message_handler(IsPrivate(), text="!publishPost", user_id=admins, state='*')
async def broadcast_post(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    data = await state.get_data()
    post_ru = data.get("Post_ru" + str(user_id))
    post_uz = data.get("Post_uz" + str(user_id))
    count = await broadcaster_text(msg_uz=post_uz, msg_ru=post_ru)
    await bot.send_message(user_id, "Number of users received msg:" + str(count))


# command for publishing forwarded messages
@dp.message_handler(IsPrivate(), text="!publishForward", user_id=admins, state='*')
async def broadcast_forwarded_post(message: types.Message, state: FSMContext):
    user_id = types.User.get_current().id
    data = await state.get_data()
    from_chat_id = data.get("Forward_from" + str(user_id))
    msg_id_uz = data.get("Forward_msg_id_uz" + str(user_id))
    msg_id_ru = data.get("Forward_msg_id_ru" + str(user_id))
    count = await broadcaster_forward(from_chat_id, msg_id_uz, msg_id_ru)
    await bot.send_message(user_id, "Number of users received msg:" + str(count))
