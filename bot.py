from aiogram.utils import executor

from create_bot import dp
from scripts import browsedriver
from handlers import client, stats
from os.path import exists
from os import mkdir


async def on_startup(_):
    if not exists("info/"):
        mkdir("info/")
        mkdir("info/images/")
        mkdir("info/json/")
    await browsedriver()
    print('bot online!')


client.register_handlers_client(dp)
stats.register_handlers_stats(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
