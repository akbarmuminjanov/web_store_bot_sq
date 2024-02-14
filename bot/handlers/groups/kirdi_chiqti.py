from loader import dp
from aiogram import types
import asyncio

@dp.message_handler(chat_type=['group', 'super_group'], content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    members = list()
    for m in message.new_chat_members:
        member = m.get_mention(as_html=True)

        members.append(m)
        welcome = await message.reply(f"Xush kelibsiz, {member}.")
        await message.delete()

        await asyncio.sleep(5)

        await message.delete(welcome)



#chiqib ketsa

@dp.message_handler(chat_type=['group', 'super_group'], content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_user(message: types.Message):

    lefted_user = message.left_chat_member.id
    admin = message.from_user.id
   
    await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} guruhni tark etdi")
        