from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import db
from keyboards import ClientKeyboard
from scripts import AnaliticStats
from handlers.utils import login_required, check_access_token


@login_required
@check_access_token
async def cmd_stats_lang(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    photo = await AnaliticStats(info["access_token"]).lang_stats()
    await msg.edit_text("📈 Ваша статистика")
    await message.answer_photo(
        photo, reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard()
    )


@login_required
@check_access_token
async def cmd_stats_os(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    photo = await AnaliticStats(info["access_token"]).os_stats()
    await msg.edit_text("📈 Ваша статистика")
    await message.answer_photo(
        photo, reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard()
    )


@login_required
@check_access_token
async def cmd_stats_editors(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    photo = await AnaliticStats(info["access_token"]).editors_stats()
    await msg.edit_text("📈 Ваша статистика")
    await message.answer_photo(
        photo, reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard()
    )


@login_required
@check_access_token
async def cmd_stats_editors(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    photo = await AnaliticStats(info["access_token"]).editors_stats()
    await msg.edit_text("📈 Ваша статистика")
    await message.answer_photo(
        photo, reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard()
    )


@login_required
@check_access_token
async def cmd_stats_categories(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    photo = await AnaliticStats(info["access_token"]).categories_stats()
    await msg.edit_text("📈 Ваша статистика")
    await message.answer_photo(
        photo, reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard()
    )


@login_required
@check_access_token
async def cmd_all_time(message: types.Message):
    msg = await message.answer("⌛ Идёт загрузка ⌛")
    info = await db.user_info(message.from_user.id)
    time = await AnaliticStats(info["access_token"]).all_time()
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
