from scripts.wakatime import wakatime_stats
import pandas as pd
from json import dump
import matplotlib.pyplot as plt
from os import remove
from os.path import exists
from datetime import datetime as dt
from io import BytesIO


class Path_files:
    PATH_JSON = "info/json/"
    PATH_IMAGES = "info/images/"
    PATH_CSV = "info/csv/"


class AnaliticStats(Path_files):
    def __init__(self):
        super(AnaliticStats, self).__init__()

    @staticmethod
    async def __record(filename, email, password):
        """Запись статистик"""
        with open(filename, "w") as f:
            dump(await wakatime_stats(email, password), f)

    @classmethod
    async def statics(cls, user_id, email, password, theme):
        """Статистика"""
        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f"{cls.PATH_JSON}{user_id}.json")
        stat = workouts["data"][theme]
        stats, times = [], []
        times.append(0)
        stats.append("Other")

        for i in stat:
            if i["total_seconds"] > 8000:
                if i["name"] != "Other":
                    times.append(i["total_seconds"])
                    stats.append(i["name"])
                else:
                    times[0] += i["total_seconds"]
            else:
                times[0] += i["total_seconds"]

        if times[0] == 0:
            del times[0]
            del stats[0]

        fig, ax = plt.subplots()
        ax.pie(times, labels=stats, shadow=True)
        ax.axis("equal")

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        img = buffer.getvalue()

        buffer.close()

        return img

    @classmethod
    async def lang_stats(cls, user_id, email, password):
        """Статистика по языкам"""
        return await cls.statics(user_id, email, password, "languages")

    @classmethod
    async def os_stats(cls, user_id, email, password):
        """Статистика по ОС"""
        return await cls.statics(user_id, email, password, "operating_systems")

    @classmethod
    async def editors_stats(cls, user_id, email, password):
        """Статистика по редакторам"""
        return await cls.statics(user_id, email, password, "editors")

    @classmethod
    async def categories_stats(cls, user_id, email, password):
        """Статистика по категориям"""
        return await cls.statics(user_id, email, password, "categories")

    @classmethod
    async def all_time(cls, user_id, email, password):
        """Все время"""

        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f"{cls.PATH_JSON}{user_id}.json")
        return workouts["data"]["human_readable_total_including_other_language"]


class NotifyStats(Path_files):
    def __init__(self):
        super(NotifyStats, self).__init__()

    @staticmethod
    async def __record(filename, email, password):
        """Запись статистик"""
        with open(filename, "w") as f:
            dump(await wakatime_stats(email, password), f)

    @classmethod
    async def statics(cls, user_id, email, password, theme):
        """Статистика"""
        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

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
