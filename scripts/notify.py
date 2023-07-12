from scripts import WakatimeStats, Visualization
from create_bot import db, bot
from asyncio import sleep
import datetime
from datetime import datetime as dt
from os import getenv


async def scheduled(self):
    while True:
        await sleep(self)
        users = await db.AllUser()
        for user in users:
            stats = WakatimeStats(
                client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET")
            )

            await db.add_stats(
                user_id=user["_id"],
                date=dt.today().strftime("%Y-%m-%d"),
                stats=await stats.get_lang_stats(user["refresh_token"]),
                theme="languages",
            )
            await db.add_stats(
                user_id=user["_id"],
                date=dt.today().strftime("%Y-%m-%d"),
                stats=await stats.get_editors_stats(user["refresh_token"]),
                theme="editors",
            )
            await db.add_stats(
                user_id=user["_id"],
                date=dt.today().strftime("%Y-%m-%d"),
                stats=await stats.get_categories_stats(user["refresh_token"]),
                theme="categories",
            )
            await db.add_stats(
                user_id=user["_id"],
                date=dt.today().strftime("%Y-%m-%d"),
                stats=await stats.get_os_stats(user["refresh_token"]),
                theme="operating_systems",
            )

        if datetime.datetime.today().isoweekday() == 7:
            for user in users:
                photo = Visualization.create_bar_diagram_slice(
                    await db.get_stats(user["_id"], "languages")
                )
                await bot.send_photo(user["_id"], photo)
