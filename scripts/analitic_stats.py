from scripts.wakatime import wakatime_stats
import pandas as pd
from json import dump
import matplotlib.pyplot as plt
from os import remove


class AnaliticStats:
    PATH_JSON = "info/json/"
    PATH_IMAGES = "info/images/"

    def __inti__(self):
        pass

    @staticmethod
    async def __record(filename, email, password):
        """Запись статистик"""
        with open(filename, 'w') as f:
            dump(await wakatime_stats(email, password), f)

    @classmethod
    async def statics(cls, user_id, email, password, theme):
        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f'{cls.PATH_JSON}{user_id}.json')
        stat = workouts["data"][theme]
        stats, times = [], []

        for i in stat:
            times.append(i["total_seconds"])
            stats.append(i["name"])

        fig, ax = plt.subplots()
        ax.pie(times, labels=stats, shadow=True)
        ax.axis("equal")
        plt.savefig(f"{cls.PATH_IMAGES}{user_id}_{theme}_stats")

        img = open(f'{cls.PATH_IMAGES}{user_id}_{theme}_stats.png', "rb")

        return img

    @classmethod
    async def lang_stats(cls, user_id, email, password):

        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f'{cls.PATH_JSON}{user_id}.json')
        yp = workouts["data"]["languages"]
        yps, times = [], []
        other = 0

        for x, i in enumerate(yp):
            if i["name"] == "Other":
                other = x

        for i in yp:
            if i["total_seconds"] > 5000:
                times.append(i["total_seconds"])
                yps.append(i["name"])
            else:
                times[other] += i["total_seconds"]

        fig, ax = plt.subplots()
        ax.pie(times, labels=yps, shadow=True)
        ax.axis("equal")
        plt.savefig(f"{cls.PATH_IMAGES}{user_id}_lang_stats")

        img = open(f'{cls.PATH_IMAGES}{user_id}_lang_stats.png', "rb")
        return img

    @classmethod
    async def os_stats(cls, user_id, email, password):
        return await cls.statics(user_id, email, password, "operating_systems")

    @classmethod
    async def editors_stats(cls, user_id, email, password):
        return await cls.statics(user_id, email, password, "editors")

    @classmethod
    async def categories_stats(cls, user_id, email, password):
        return await cls.statics(user_id, email, password, "categories")

    @classmethod
    async def all_time(cls, user_id, email, password):

        await cls.__record(f"{cls.PATH_JSON}{user_id}.json", email, password)

        workouts = pd.read_json(f"{cls.PATH_JSON}{user_id}.json")
        remove(f'{cls.PATH_JSON}{user_id}.json')
        return workouts["data"]["human_readable_total_including_other_language"]
