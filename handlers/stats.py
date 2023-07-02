from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import db
from keyboards import kb_client
from scripts import AnaliticStats


async def cmd_stats_lang(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await AnaliticStats.lang_stats(info["_id"], info["refresh_token"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(
            photo, reply_markup=await kb_client(await db.userExsist(message.from_id))
        )


async def cmd_stats_os(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await AnaliticStats.os_stats(info["_id"], info["refresh_token"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(
            photo, reply_markup=await kb_client(await db.userExsist(message.from_id))
        )


async def cmd_stats_editors(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await AnaliticStats.editors_stats(info["_id"], info["refresh_token"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(
            photo, reply_markup=await kb_client(await db.userExsist(message.from_id))
        )


async def cmd_stats_editors(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await AnaliticStats.editors_stats(info["_id"], info["refresh_token"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(
            photo, reply_markup=await kb_client(await db.userExsist(message.from_id))
        )


async def cmd_stats_categories(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        photo = await AnaliticStats.categories_stats(info["_id"], info["refresh_token"])
        await msg.edit_text(f"📈 Ваша статистика")
        await message.answer_photo(
            photo, reply_markup=await kb_client(await db.userExsist(message.from_id))
        )


async def cmd_all_time(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        time = await AnaliticStats.all_time(info["_id"], info["refresh_token"])
        await msg.edit_text(f"⌛ {time}")


def register_handlers_stats(dp: Dispatcher):
    dp.register_message_handler(cmd_stats_lang, Text(equals="Статистика по языкам"))
    dp.register_message_handler(cmd_stats_os, Text(equals="Статистика по ос"))
    dp.register_message_handler(
        cmd_stats_editors, Text(equals="Статистика по редакторам")
    )
    dp.register_message_handler(
        cmd_stats_categories, Text(equals="Статистика по категориям")
    )
    dp.register_message_handler(cmd_all_time, Text(equals="Всё время"))
