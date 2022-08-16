from aiogram.utils import executor

from create_bot import dp
from scripts import browsedriver
from handlers import client, stats


async def on_startup(_):
    await browsedriver()
    print('bot online!')


client.register_handlers_client(dp)
stats.register_handlers_stats(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
