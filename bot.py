from aiogram.utils.executor import start_polling
from asyncio import new_event_loop, set_event_loop

from create_bot import dp
from handlers import client, stats
from os.path import exists
from os import mkdir
from logging import basicConfig, INFO
from datetime import datetime as dt
from scripts.notify import scheduled


async def on_startup(_):
    if not exists("logs/"):
        mkdir("logs/")
    basicConfig(
        filename=f'logs/[{dt.today().strftime("%Y-%m-%d-%H")}].log',
        filemode="a",
        level=INFO,
    )
    print("bot online!")


client.register_handlers_client(dp)
stats.register_handlers_stats(dp)


if __name__ == "__main__":
    loop = new_event_loop()
    set_event_loop(loop)
    loop.create_task(scheduled(86400))
    start_polling(dp, skip_updates=True, on_startup=on_startup)
