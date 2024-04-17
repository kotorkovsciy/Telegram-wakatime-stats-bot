from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from keyboards import ClientKeyboard
from create_bot import db
from scripts import WakatimeAPI
from os import getenv


class Auth(StatesGroup):
    code = State()
    check = State()


async def cmd_start(message: types.Message):
    await message.answer(
        "Привет я бот StatsWakaTime, и предоставляю вашу статистику с сайта WakaTime.com",
        reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "❗ Действие отменено",
        reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
    )


async def cmd_clb_cancel(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.delete()
    await query.message.answer(
        "❗ Действие отменено",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await query.message.answer(
        "Для продолжения работы используйте кнопки 👇",
        reply_markup=await ClientKeyboard(query.from_user.id).get_keyboard(),
    )


async def auth_step(message: types.Message, state: FSMContext):
    temp_msg = await message.answer(
        "⌛ Идёт загрузка... ⌛", reply_markup=types.ReplyKeyboardRemove()
    )
    await Auth.code.set()
    await state.update_data(user_id=message.from_user.id)
    auth_url = WakatimeAPI(
        client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET")
    ).get_url_auth()
    await temp_msg.delete()
    await message.answer(
        "Чтобы авторизоваться, перейдите поссылке и введите сюда токен",
        reply_markup=await ClientKeyboard.kb_auth_url(auth_url),
    )


async def res_step(message: types.Message, state: FSMContext):
    await Auth.check.set()
    msg = await message.answer("⌛ Производится авторизация ⌛")
    await state.update_data(code=message.text)
    api = WakatimeAPI(client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET"))
    user_data = await state.get_data()
    if api.set_auth_session(user_data["code"]):
        refresh_token = api.get_refresh_token()
        access_token = api.get_access_token()
        await db.user_add(user_data["user_id"], refresh_token, access_token)
        await msg.edit_text("✅ Авторизация прошла успешно")
        await message.answer(
            "Для просмотра статистик используйте кнопки 👇",
            reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
        )
    else:
        await msg.edit_text("❌ Авторизация не пройдена")
        await message.answer(
            "❗ Имя пользователя или пароль введены неверно",
            reply_markup=await ClientKeyboard.kb_auth(),
        )
    await state.finish()


async def cmd_exit(message: types.Message):
    if not await db.user_exsist(message.from_user.id):
        await message.answer(
            "❗ Вы не авторизованны",
            reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
        )
    else:
        await db.user_del(message.from_user.id)
        await message.answer(
            "❗ Вы успешно вышли из аккаунта",
            reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_cancel, commands="Отмена", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
    dp.register_callback_query_handler(cmd_clb_cancel, Text(equals="cancel"), state="*")
    dp.register_message_handler(auth_step, Text(equals="Авторизация"), state="*")
    dp.register_message_handler(
        res_step, state=Auth.code, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(cmd_exit, Text(equals="Выход"))
