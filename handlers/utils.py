from keyboards import ClientKeyboard
from aiogram import types
from create_bot import db


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
