from sqlalchemy import (Column, String, BigInteger, Boolean, ForeignKey, DateTime, func, Integer, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import sql
from utils.db_api.database import db


# Creating User Model
class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    # telegram chat_id of user
    chat_id = Column(BigInteger, primary_key=True)

    # language selected by user
    lang = Column(String(2), default='uz')

    # Created_at date when user created account
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Requested_at this is time when user changed their language
    requested_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<User(chat_id='{}', language='{}')>".format(
            self.chat_id, self.lang)


# Creating Services Model
class Service(db.Model):
    __tablename__ = 'services'
    query: sql.select

    # Identifier of service
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Activated service for Main Menu
    is_active = Column(Boolean, default=False)

    # Many Services have one user : One to Many Relationship According to User, User has many Services
    user_chat_id = Column(BigInteger, ForeignKey('users.chat_id', ondelete="cascade"))

    # Login to keep the personal account number
    login = Column(String(100))

    # Auth_token permanent token which will give us to access user's data in api
    auth_token = Column(String(150))

    # Service Type individual:1, business:2
    type = Column(Integer)

    # Created_at date when user connect this particular Service
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Requested_at this is time when user request's this particular service for activity analysis of user
    requested_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Service(user_chat_id='{}', login='{}', type='{}')>".format(
            self.user_chat_id, self.login, self.type)


