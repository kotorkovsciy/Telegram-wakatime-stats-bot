from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import db
from keyboards import kb_client
from scripts import lang_stats
from os import remove


async def cmd_stats_lang(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(f"❗ Вы не авторизованны", reply_markup=await kb_client(await db.userExsist(message.from_id)))
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await lang_stats(info["_id"], info["email"], info["password"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(photo, reply_markup=await kb_client(await db.userExsist(message.from_id)))
        remove(f'{message.from_user.id}.png')


def register_handlers_stats(dp: Dispatcher):
    dp.register_message_handler(
        cmd_stats_lang, Text(equals='Статистика по яп'))
