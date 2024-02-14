import asyncio
import datetime

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot

@dp.message_handler(IsGroup(), Command("limit", prefixes="!/"), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    
   
    

    time = int(message.text[9:])
    
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    try:
        await message.chat.restrict(user_id=member_id, can_send_messages=False, until_date=until_date)
        await message.reply_to_message.delete()
    except aiogram.utils.exceptions.BadRequest as err:
        await message.answer(f"Xatolik! {err.args}")
        return

    ban_message = await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} {time} minut yozish huquqidan mahrum qilindi."
                        )

    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")
    # 5 sekun kutib xabarlarni o'chirib tashlaymiz
    await asyncio.sleep(5)
    await message.delete()
    await ban_message.delete()
    await service_message.delete()  

@dp.message_handler(IsGroup(), Command("limit_boom", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    service_message = await message.reply(f"Foydalanuvchi {member.full_name} tiklandi")

    # xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)

    service_message = await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} guruhdan haydaldi")
     
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()