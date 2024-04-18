redesigned weekly newsletterfrom scripts import WakatimeStats, Visualization
from datetime import datetime as dt
from celery import Celery
from celery.schedules import crontab
from os import getenv
from scripts import Database
from aiogram import Bot
import asyncio

from dotenv import load_dotenv

load_dotenv()

app = Celery(
    "tasks",
    broker=getenv("RABBITMQ_URI"),
)

async def _execute_update_stats() -> None:
    db = Database(getenv("CONNECTIONSTRING"))
    users = await db.all_user()

    for user in users:

        stats = WakatimeStats(access_token=user["access_token"])

        await db.add_stats(
            user_id=user["_id"],
            date=dt.today().strftime("%Y-%m-%d"),
            stats=await stats.get_lang_stats(),
            theme="languages",
        )
        await db.add_stats(
            user_id=user["_id"],
            date=dt.today().strftime("%Y-%m-%d"),
            stats=await stats.get_editors_stats(),
            theme="editors",
        )
        await db.add_stats(
            user_id=user["_id"],
            date=dt.today().strftime("%Y-%m-%d"),
            stats=await stats.get_categories_stats(),
            theme="categories",
        )
        await db.add_stats(
            user_id=user["_id"],
            date=dt.today().strftime("%Y-%m-%d"),
            stats=await stats.get_os_stats(),
            theme="operating_systems",
        )

async def _execute_mailing() -> None:
    bot = Bot(token=getenv("TOKEN"))
    db = Database(getenv("CONNECTIONSTRING"))
    users = await db.all_user()
    for user in users:
        photo = Visualization.create_bar_diagram_slice(
                await db.get_stats(user["_id"], "languages")
        )
        await bot.send_message(user["_id"], "Еженедельная статистика")
        await bot.send_photo(user["_id"], photo)
    await bot.close()

asyncio.run(_execute_update_stats())

@app.task()
def execute_update_stats() -> None:
    asyncio.run(_execute_update_stats())

@app.task()
def execute_mailing() -> None:
    asyncio.run(_execute_mailing())

app.conf.beat_schedule = {
    "task_execute_mailing": {
        "task": "tasks.execute_mailing",
        "schedule": crontab(minute=0, hour=14, day_of_month='*', month_of_year='*', day_of_week='*/4'),
    },
    "task_execute_update_stats": {
        "task": "tasks.execute_update_stats",
        "schedule": crontab(minute=0, hour=8, day_of_month='*', month_of_year='*', day_of_week='*/7'),
    }
}

app.conf.timezone = "Europe/Moscow"
