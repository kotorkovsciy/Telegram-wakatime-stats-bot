from scripts import NotifyStats
from create_bot import db, bot
from asyncio import sleep
import datetime


async def scheduled(self):
    while True:
        await sleep(self)
        users = await db.AllUser()
        for user in users:
            await NotifyStats.statics(user["_id"], user["refresh_token"], "languages")
            await NotifyStats.statics(user["_id"], user["refresh_token"], "editors")
            await NotifyStats.statics(user["_id"], user["refresh_token"], "categories")
            await NotifyStats.statics(
                user["_id"], user["refresh_token"], "operating_systems"
            )
            await NotifyStats.processing_statistics(user["_id"], "languages")
            await NotifyStats.processing_statistics(user["_id"], "editors")
            await NotifyStats.processing_statistics(user["_id"], "categories")
            await NotifyStats.processing_statistics(user["_id"], "operating_systems")
        if datetime.datetime.today().isoweekday() == 7:
            for user in users:
                photo = await NotifyStats.visualize(user["_id"], "languages")
                await bot.send_photo(user["_id"], photo)
