from keyboards import ClientKeyboard
from aiogram import types
from create_bot import db
from scripts import WakatimeAPI
from os import getenv


def login_required(func):
    async def wrapper(message: types.Message):
        if not await db.userExsist(message.from_user.id):
            await message.answer(
                "❗ Вы не авторизованны",
                reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
            )
        else:
            await func(message)

    return wrapper


def check_refresh_token(func):
    """Decorator for check refresh token

    Args:
        func (func): Function for check refresh token

    Returns:
        func: Wrapper for check refresh token
    """

    async def wrapper(message: types.Message):
        api = WakatimeAPI(client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET"))

        info = await db.userInfo(message.from_user.id)

        check = api.check_refresh_token(info["refresh_token"])

        if check:
            await func(message)
        else:
            db.userUpdate(message.from_user.id, api.get_refresh_token())
            await func(message)

    return wrapper
