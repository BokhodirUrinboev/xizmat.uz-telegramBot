from aiogram import types
from sqlalchemy import and_
from utils.db_api.models import User, Service
from utils.db_api.database import db


class DBCommands:
    # function to get user object
    async def get_user(self, chat_id):
        # Getting object of user where chat_id is given
        user = await User.query.where(User.chat_id == chat_id).gino.first()
        return user

    async def get_all_users(self):
        # Getting object of user where chat_id is given
        users = await User.query.gino.all()
        return users

    # function to create user object if it exists in database it will return user object otherwise new user will be
    # created and returned
    async def add_new_user(self):
        # it gets current user which called this function
        user = types.User.get_current()

        # create new user
        new_user = User()

        # assign chat id to this user
        new_user.chat_id = user.id
        if user.locale in ['ru', 'uz']:
            new_user.lang = user.locale
        else:
            new_user.lang = 'uz'
        # creating user
        await new_user.create()
        return new_user

    # Function to set language for particular user
    async def set_language(self, user_id, language):

        # getting current user
        user = await self.get_user(user_id)
        if user:
            # updating it is language
            await user.update(lang=language).apply()
        else:
            user = await self.add_new_user()
            await user.update(lang=language).apply()

    # Function to identify user's language
    async def get_language(self, chat_id):
        # From database getting user
        user = await self.get_user(chat_id)
        if user:
            # if user exist returning it's language
            return user.lang

    # Function to count number of users in database
    async def count_users(self) -> int:
        # from database count user id in users table
        total = await db.func.count(User.chat_id).gino.scalar()
        return total

    # Create account
    async def add_service(self, user_chat_id, login, login_type, auth_token):
        user = self.get_user(user_chat_id)
        if user is None:
            user = types.User.get_current()
            new_user = User()

            # assign chat id to this user
            new_user.chat_id = user_chat_id
            if user.locale in ['ru', 'uz']:
                new_user.lang = user.locale
            else:
                new_user.lang = 'uz'
            # creating user
            await new_user.create()
            new_service = Service()
            new_service.user_chat_id = user_chat_id
            new_service.login = login
            new_service.type = login_type
            new_service.auth_token = auth_token
            await new_service.create()
            return new_service
        else:
            new_service = Service()
            new_service.user_chat_id = user_chat_id
            new_service.login = login
            new_service.type = login_type
            new_service.auth_token = auth_token
            await new_service.create()
            return new_service

    # returning particular service by id
    async def get_service(self, service_id):
        service = await Service.query.where(Service.id == service_id).gino.first()
        return service

    # returning all services of particular user
    async def get_all_services(self, user_chat_id):
        services = await Service.query.where(Service.user_chat_id == user_chat_id).gino.all()
        return services

    # returning active service of particular user
    async def get_active_service(self, user_id):
        services = await Service.query.where(Service.user_chat_id == user_id).gino.all()
        for service in services:
            if service.is_active:
                return service
        return None

    async def get_user_by_service_login(self, user_login):
        services = await Service.query.where(Service.login == user_login).gino.all()
        for service in services:
            if service.is_active:
                return service
        return None

    # modifying active service
    async def modify_active_service(self, user_id, service_id):
        old_active_service = await self.get_active_service(user_id)
        if old_active_service:
            await old_active_service.update(is_active=False).apply()
        new_active_service = await self.get_service(service_id)
        await new_active_service.update(is_active=True).apply()
        return new_active_service

    # remove service
    async def remove_service(self, service_id):
        service = await Service.delete.where(Service.id == service_id).gino.status()
        return service
