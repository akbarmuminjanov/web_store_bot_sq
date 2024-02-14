import asyncpg

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot

from keyboards.default.buttons import menu
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except:
        user = db.select_user(id=message.from_user.id)

    await message.answer("Xush kelibsiz!", reply_markup=menu)

    count = db.count_users()
    msg = f"{user[0]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
    