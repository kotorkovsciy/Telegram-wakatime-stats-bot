from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from keyboards import kb_client, kb_cancel
from create_bot import db
from scripts import WakatimeAPI
from os import getenv


class Auth(StatesGroup):
    code = State()


async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет я бот StatsWakaTime, и предоставляю вашу статистику с сайта WakaTime.com",
        reply_markup=await kb_client(await db.userExsist(message.from_id)),
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "❗ Действие отменено",
        reply_markup=await kb_client(await db.userExsist(message.from_id)),
    )


async def auth_step(message: types.Message, state: FSMContext):
    await Auth.code.set()
    await state.update_data(user_id=message.from_user.id)
    auth_url = WakatimeAPI(
        client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET")
    ).get_url_auth()
    await message.answer(
        "Чтобы авторизоваться, перейдите поссылке и введите сюда токен " + auth_url,
        reply_markup=kb_cancel,
    )


async def res_step(message: types.Message, state: FSMContext):
    msg = await message.answer("⌛ Производится авторизация ⌛")
    await state.update_data(code=message.text)
    api = WakatimeAPI(client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET"))
    user_data = await state.get_data()
    if api.set_auth_session(user_data["code"]):
        refresh_token = api.get_refresh_token()
        await db.userAdd(user_data["user_id"], refresh_token)
        await msg.edit_text("✅ Авторизация прошла успешно")
        await message.answer(
            "Для просмотра статистик используйте кнопки 👇",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        await msg.edit_text("❌ Авторизация не пройдена")
        await message.answer(
            "❗ Имя пользователя или пароль введены неверно",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    await state.finish()


async def cmd_exit(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        await db.userDel(message.from_user.id)
        await message.answer(
            "❗ Вы успешно вышли из аккаунта",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_cancel, commands="Отмена", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
    dp.register_message_handler(auth_step, Text(equals="Авторизация"), state="*")
    dp.register_message_handler(
        res_step, state=Auth.code, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(cmd_exit, Text(equals="Выход"))
