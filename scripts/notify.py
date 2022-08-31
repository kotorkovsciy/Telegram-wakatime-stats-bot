from scripts import NotifyStats
from create_bot import db, bot
from asyncio import sleep
import datetime


async def scheduled(self):
    while True:
        await sleep(self)
        users = await db.AllUser()
        for user in users:
            await NotifyStats.statics(
                user["_id"], user["email"], user["password"], "languages"
            )
            await NotifyStats.statics(
                user["_id"], user["email"], user["password"], "editors"
            )
            await NotifyStats.statics(
                user["_id"], user["email"], user["password"], "categories"
            )
            await NotifyStats.statics(
                user["_id"], user["email"], user["password"], "operating_systems"
            )
            await NotifyStats.processing_statistics(user["_id"], "languages")
            await NotifyStats.processing_statistics(user["_id"], "editors")
            await NotifyStats.processing_statistics(user["_id"], "categories")
            await NotifyStats.processing_statistics(user["_id"], "operating_systems")
        if datetime.datetime.today().isoweekday() == 7:
            for user in users:
                photo = await NotifyStats.visualize(user["_id"], "languages")
                await bot.send_photo(user["_id"], photo)
