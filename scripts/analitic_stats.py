from scripts.wakatime import wakatime_stats
import pandas as pd
import json
import matplotlib.pyplot as plt
from os import remove


async def record(filename, email, password):
    """Запись статистик"""
    with open(filename, 'w') as f:
        json.dump(await wakatime_stats(email, password), f)


async def lang_stats(user_id, email, password):

    await record(f"{user_id}.json", email, password)

    workouts = pd.read_json(f"{user_id}.json")
    remove(f'{user_id}.json')
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
    plt.savefig(f"{user_id}")

    img = open(f'{user_id}.png', "rb")
    return img
