from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


but_reg = KeyboardButton('Авторизация')
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reg.add(but_reg)


but_stat_yp = KeyboardButton('Статистика по яп')
but_stat_os = KeyboardButton('Статистика по ос')
kb_stats = ReplyKeyboardMarkup(resize_keyboard=True)
kb_stats.add(but_stat_yp).add(but_stat_os)


async def kb_client(Krivda):
    if not Krivda:
        return kb_reg
    else:
        return kb_stats


but_cancel = KeyboardButton('Отмена')

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(but_cancel)
