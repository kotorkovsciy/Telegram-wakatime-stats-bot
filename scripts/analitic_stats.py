from scripts.wakatime import WakatimeAPI, WakatimeStats
from scripts.visualization import Visualization
import pandas as pd
from json import dump
import matplotlib.pyplot as plt
from os import remove, getenv
from os.path import exists
from datetime import datetime as dt
from io import BytesIO


class Path_files:
    PATH_JSON = "info/json/"
    PATH_IMAGES = "info/images/"
    PATH_CSV = "info/csv/"


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


class NotifyStats(Path_files):
    def __init__(self):
        super(NotifyStats, self).__init__()

    @staticmethod
    async def __record(filename, refresh_token):
        """Запись статистик"""
        with open(filename, "w") as f:
            api = WakatimeStats(
                client_id=getenv("CLIENT_ID"), client_secret=getenv("SECRET")
            )
            api._new_refresh_session(refresh_token)
            dump(api.get_stats(), f)

    @classmethod
    async def statics(cls, user_id, refresh_token, theme):
        """Статистика"""
        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", refresh_token)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f"{cls.PATH_JSON}{user_id}.json")
        stat = workouts["data"][theme]
        stats, times = [], []

        for i in stat:
            times.append(i["total_seconds"])
            stats.append(i["name"])

        data = {}

        data["time"] = dt.today().strftime("%Y-%m-%d")

        for i in stat:
            data[i["name"]] = i["total_seconds"]

        if not exists(f"{cls.PATH_CSV}{user_id}_{theme}_stats.csv"):
            df = pd.DataFrame()
            df = df.append(data, ignore_index=True)
        else:
            df = pd.read_csv(f"{cls.PATH_CSV}{user_id}_{theme}_stats.csv", index_col=0)
            df = df.append(data, ignore_index=True)
        df.to_csv(f"{cls.PATH_CSV}{user_id}_{theme}_stats.csv")
        return True

    @classmethod
    async def visualize(cls, user_id, theme):
        """Визуализация"""
        df = pd.read_csv(
            f"{cls.PATH_CSV}{user_id}_{theme}_proc_stats.csv",
            parse_dates=["time"],
            index_col=0,
        )
        print(
            f"{dt.today().strftime('%Y-%m-%d-%H.%M.%S')}] visualize: начато визуализацию данных"
        )
        df2 = pd.DataFrame(df.mean(numeric_only=True)[0:5])
        df["time"] = df["time"].dt.strftime("%m/%d/%Y")
        df.plot(x="time", y=df2.index, kind="bar")
        plt.savefig(f"{cls.PATH_IMAGES}{user_id}_{theme}_n_stats.png")
        img = open(f"{cls.PATH_IMAGES}{user_id}_{theme}_n_stats.png", "rb")
        print(
            f"{dt.today().strftime('%Y-%m-%d-%H.%M.%S')}] visualize: закончено визуализацию данных"
        )
        return img

    @classmethod
    async def processing_statistics(cls, user_id, theme):
        """Обработка статистики"""
        df = pd.read_csv(
            f"{cls.PATH_CSV}{user_id}_{theme}_stats.csv",
            parse_dates=["time"],
            index_col=0,
        )
        print(
            f'[{dt.today().strftime("%Y-%m-%d-%H.%M.%S")}] analitic: открыт датафрейм {user_id}_{theme}_stats.csv'
        )
        for index, row in df.iterrows():
            data = {}
            sum = 0
            for i in row.items():
                if i[0] != "time":
                    sum += float(i[1])

            for i in row.items():
                if i[0] != "time":
                    data[i[0]] = float(i[1]) / sum * 100
                else:
                    data[i[0]] = i[1]

            if not exists(f"{cls.PATH_CSV}{user_id}_{theme}_proc_stats.csv"):
                df = pd.DataFrame()
                df = df.append(data, ignore_index=True)
            else:
                df = pd.read_csv(
                    f"{cls.PATH_CSV}{user_id}_{theme}_proc_stats.csv", index_col=0
                )
                df = df.append(data, ignore_index=True)
            df.to_csv(f"{cls.PATH_CSV}{user_id}_{theme}_proc_stats.csv")
        print(
            f"[{dt.today().strftime('%Y-%m-%d-%H.%M.%S')}] analitic: закрыт датафрейм {user_id}_{theme}_stats.csv"
        )
        return True
