from scripts.wakatime import WakatimeStats
from scripts.visualization import Visualization
from os import getenv


class AnaliticStats:
    def __init__(self):
        self.stats = WakatimeStats(
            client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET")
        )

    async def lang_stats(self, refresh_token):
        """Статистика по языкам"""

        data = await self.stats.get_lang_stats(refresh_token)

        return Visualization.create_pie_diagram(data)

    async def os_stats(self, refresh_token):
        """Статистика по ОС"""

        data = await self.stats.get_os_stats(refresh_token)

        return Visualization.create_pie_diagram(data)

    async def editors_stats(self, refresh_token):
        """Статистика по редакторам"""

        data = await self.stats.get_editors_stats(refresh_token)

        return Visualization.create_pie_diagram(data)

    async def categories_stats(self, refresh_token):
        """Статистика по категориям"""

        data = await self.stats.get_categories_stats(refresh_token)

        return Visualization.create_pie_diagram(data)

    async def all_time(self, refresh_token):
        """Все время"""

        return await self.stats.get_all_time(refresh_token)
