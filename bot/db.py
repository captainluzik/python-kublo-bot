from typing import Optional, Sequence

from aiogram import types
from sqlalchemy import (
    Column, Integer, String, select, insert, literal_column, update, BigInteger
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base

from settings import DATABASE_URI

Base = declarative_base()

engine: Optional[AsyncEngine] = None


async def init_database():
    global engine
    engine = create_async_engine(DATABASE_URI, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def stop_database():
    if engine:
        await engine.dispose()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegramID = Column(BigInteger, nullable=False)
    username = Column(String(32), nullable=True)
    first_name = Column(String(32), nullable=True)
    last_name = Column(String(32), nullable=True)
    chatID = Column(BigInteger, nullable=True)
    stars = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name})>"


async def save_user(message: types.Message) -> User:
    user_id = int(message.from_user.id)
    chat_id = int(message.chat.id)
    username = message.from_user.username if message.from_user.username else None
    first_name = message.from_user.first_name if message.from_user.first_name else None
    last_name = message.from_user.last_name if message.from_user.last_name else None

    async with engine.begin() as conn:
        stmt = select(User).where(User.telegramID == user_id, User.chatID == chat_id)
        result = await conn.execute(stmt)
        user = result.fetchone()

        if not user:
            stmt = insert(User).values(
                telegramID=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                chatID=chat_id
            ).returning(literal_column("*"))
            result = await conn.execute(stmt)
            user = result.fetchone()

        print(f"user: {user}")
        return user


async def get_user(message: types.Message) -> User:
    user_id = int(message.from_user.id)
    chat_id = int(message.chat.id)
    print(f"user_id: {user_id}")
    print(f"chat_id: {chat_id}")
    async with engine.begin() as conn:
        stmt = select(User).where(User.telegramID == user_id, User.chatID == chat_id)
        result = await conn.execute(stmt)
        print(f"result: {result}")
        user = result.fetchone()
        return user


async def add_star(message: types.Message):
    reply_to_message = message.reply_to_message
    if reply_to_message:
        user = await get_user(reply_to_message)
        print(f"user: {user}")
        if user:
            async with engine.begin() as conn:
                stmt = (
                    update(User)
                    .values(stars=user.stars + 1)
                    .where(User.telegramID == user.telegramID)
                    .returning(literal_column("*"))
                )
                result = await conn.execute(stmt)
                user = result.fetchone()
                return user
        else:
            return None


async def minus_star(message: types.Message):
    reply_to_message = message.reply_to_message
    if reply_to_message:
        user = await get_user(reply_to_message)
        print(f"user: {user}")
        if user:
            async with engine.begin() as conn:
                stmt = (
                    update(User)
                    .values(stars=user.stars - 1)
                    .where(User.telegramID == user.telegramID)
                    .returning(literal_column("*"))
                )
                result = await conn.execute(stmt)
                user = result.fetchone()
                return user
        else:
            return None


async def get_top_users(message: types.Message):
    chat_id = int(message.chat.id)
    async with engine.begin() as conn:
        stmt = select(User).where(User.chatID == chat_id).order_by(User.stars.desc())
        result = await conn.execute(stmt)
        users = result.fetchall()
        return users


async def get_all_chat_users(message: types.Message) -> Sequence[User]:
    chat_id = int(message.chat.id)
    async with engine.begin() as conn:
        stmt = select(User).filter_by(chatID=chat_id)
        result = await conn.execute(stmt)
        return result.fetchall()
