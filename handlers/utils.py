from keyboards import ClientKeyboard
from aiogram import types
from create_bot import db
from scripts import WakatimeAPI
from os import getenv


def login_required(func):
    async def wrapper(message: types.Message):
        if not await db.user_exsist(message.from_user.id):
            await message.answer(
                "❗ Вы не авторизованны",
                reply_markup=await ClientKeyboard(message.from_user.id).get_keyboard(),
            )
        else:
            await func(message)

    return wrapper

def check_access_token(func):
    """Decorator for check access token
    
    Args:
        func (func): Function for check access token

    Returns:
        func: Wrapper for check access token
    """

    async def wrapper(message: types.Message):
        api = WakatimeAPI(client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET"))

        info = await db.user_info(message.from_user.id)

        check = api.check_access_token(info['access_token'])

        if check:
            await func(message)
        else:
            db.user_update(message.from_user.id, api.get_refresh_token(), api.get_access_token())
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

        info = await db.user_info(message.from_user.id)

        check = api.check_refresh_token(info["refresh_token"])

        if check:
            await func(message)
        else:
            db.user_update(message.from_user.id, api.get_refresh_token(), api.get_access_token())
            await func(message)

    return wrapper
