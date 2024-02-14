from aiogram import types

from loader import dp


# from aiogram.dispatcher.filters import AdminFilter as AF
                                        # ,content_types = "any"
# Echo bot
@dp.message_handler(chat_type="private")
async def bot_echo(message: types.Message):
    await message.answer(message.text)
