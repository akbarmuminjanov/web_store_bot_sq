import io

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import AdminFilter
from loader import dp, bot


@dp.message_handler(Command("set_photo", prefixes="!/"), AdminFilter(is_chat_admin=True), chat_type=['group'])
async def set_new_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(photo)
 
    await message.chat.set_photo(photo=input_file)



@dp.message_handler(Command("set_title", prefixes="!/"), AdminFilter(is_chat_admin=True), chat_type=['group'])
async def set_new_title(message: types.Message):
    text = message.text
    title = text[13:]
    #2-usul
    await message.chat.set_title(title)

@dp.message_handler(Command("set_desc", prefixes="!/"), AdminFilter(is_chat_admin=True), chat_type=['group'])
async def set_new_desc(message: types.Message):
    text = message.text
    description = text[12:]
    #2-usul
    await message.chat.set_description(description)