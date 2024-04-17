from scripts.wakatime import WakatimeStats
from scripts.visualization import Visualization


class AnaliticStats:
    def __init__(self, access_token: str):
        self.stats = WakatimeStats(access_token)

    async def lang_stats(self):
        """Статистика по языкам"""

        data = await self.stats.get_lang_stats()

        return Visualization.create_pie_diagram(data)

    async def os_stats(self):
        """Статистика по ОС"""

        data = await self.stats.get_os_stats()

        return Visualization.create_pie_diagram(data)

    async def editors_stats(self):
        """Статистика по редакторам"""

        data = await self.stats.get_editors_stats()

        return Visualization.create_pie_diagram(data)

    async def categories_stats(self):
        """Статистика по категориям"""

        data = await self.stats.get_categories_stats()

        return Visualization.create_pie_diagram(data)

    async def all_time(self):
        """Все время"""

        return await self.stats.get_all_time()
