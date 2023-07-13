from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
from create_bot import db


class ClientKeyboard:
    """Keyboard for client"""

    __BTN_AUTH: Final[KeyboardButton] = KeyboardButton("Авторизация")
    __KB_AUTH: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    __KB_AUTH.add(__BTN_AUTH)

    __BTN_ALL_TIME: Final[KeyboardButton] = KeyboardButton("Всё время")
    __BTN_STAT_LANG: Final[KeyboardButton] = KeyboardButton("Статистика по языкам")
    __BTN_STAT_OS: Final[KeyboardButton] = KeyboardButton("Статистика по ос")
    __BTN_STAT_EDITORS: Final[KeyboardButton] = KeyboardButton(
        "Статистика по редакторам"
    )
    __BTN_STAT_CATEGORIES: Final[KeyboardButton] = KeyboardButton(
        "Статистика по категориям"
    )
    __BTN_EXIT: Final[KeyboardButton] = KeyboardButton("Выход")

    __BTN_CANCEL: Final[KeyboardButton] = KeyboardButton("Отмена")
    __KB_CANCEL: Final[ReplyKeyboardMarkup] = ReplyKeyboardMarkup(resize_keyboard=True)
    __KB_CANCEL.add(__BTN_CANCEL)

    def __init__(self, user_id: int):
        """Init

        :param user_id: ID user
        :type user_id: int

        :return: None
        :rtype: None
        """

        self.__user_id = user_id

    async def get_keyboard(self) -> ReplyKeyboardMarkup:
        """Return keyboard

        :return: Keyboard

        :rtype: ReplyKeyboardMarkup
        """

        if await db.user_exsist(self.__user_id):
            return await self.kb_stats()

        return await self.kb_auth()

    @classmethod
    async def kb_stats(cls) -> ReplyKeyboardMarkup:
        """Return keyboard with stats

        :return: Keyboard

        :rtype: ReplyKeyboardMarkup
        """

        kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

        kb.add(
            cls.__BTN_ALL_TIME,
            cls.__BTN_STAT_LANG,
            cls.__BTN_STAT_OS,
            cls.__BTN_STAT_EDITORS,
            cls.__BTN_STAT_CATEGORIES,
            cls.__BTN_EXIT,
        )

        return kb

    @classmethod
    async def kb_cancel(cls) -> ReplyKeyboardMarkup:
        """Keyboard with button cancel

        :return: Keyboard

        :rtype: ReplyKeyboardMarkup
        """

        return cls.__KB_CANCEL

    @classmethod
    async def kb_auth(cls) -> ReplyKeyboardMarkup:
        """Keyboard with button auth

        :return: Keyboard

        :rtype: ReplyKeyboardMarkup
        """

        return cls.__KB_AUTH

    @classmethod
    async def kb_auth_url(cls, url: str) -> InlineKeyboardMarkup:
        """Keyboard with button auth

        :return: Keyboard

        :rtype: ReplyKeyboardMarkup
        """

        kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Получить токен", url=url))
        kb.add(InlineKeyboardButton("Отмена", callback_data="cancel"))

        return kb
