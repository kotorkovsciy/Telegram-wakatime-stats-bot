from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


but_reg = KeyboardButton('Авторизация')
kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reg.add(but_reg)


but_all_time = KeyboardButton('Всё время')
but_stat_lang = KeyboardButton('Статистика по языкам')
but_stat_os = KeyboardButton('Статистика по ос')
but_stat_editors = KeyboardButton('Статистика по редакторам')
but_stat_categories = KeyboardButton('Статистика по категориям')
kb_stats = ReplyKeyboardMarkup(resize_keyboard=True)
kb_stats.add(but_all_time).add(but_stat_lang).add(but_stat_os)\
    .add(but_stat_editors).add(but_stat_categories)


async def kb_client(Krivda):
    if not Krivda:
        return kb_reg
    else:
        return kb_stats


but_cancel = KeyboardButton('Отмена')

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(but_cancel)
