from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import db
from keyboards import kb_client
from scripts import lang_stats
from os import remove


async def cmd_stats_lang(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(f"Вы не зарегистрированы", reply_markup=await kb_client(await db.userExsist(message.from_id)))
    else:
        await message.answer(f"Ваша статистика", reply_markup=await kb_client(await db.userExsist(message.from_id)))
        info = await db.userInfo(message.from_user.id)
        await message.answer_photo(await lang_stats(info["_id"], info["email"], info["password"]), reply_markup=await kb_client(await db.userExsist(message.from_id)))
        remove(f'{message.from_user.id}.png')


def register_handlers_stats(dp: Dispatcher):
    dp.register_message_handler(
        cmd_stats_lang, Text(equals='Статистика по яп'))
