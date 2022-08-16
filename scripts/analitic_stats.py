from scripts.wakatime import wakatime_stats
import pandas as pd
from json import dump
import matplotlib.pyplot as plt
from os import remove


async def record(filename, email, password):
    """Запись статистик"""
    with open(filename, 'w') as f:
        dump(await wakatime_stats(email, password), f)


async def lang_stats(user_id, email, password):

    await record(f"info/json/{user_id}.json", email, password)

    workouts = pd.read_json(f"info/json/{user_id}.json")
    remove(f'info/json/{user_id}.json')
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
    plt.savefig(f"info/images/{user_id}_lang_stats")

    img = open(f'info/images/{user_id}_lang_stats.png', "rb")
    return img


async def os_stats(user_id, email, password):

    await record(f"info/json/{user_id}.json", email, password)

    workouts = pd.read_json(f"info/json/{user_id}.json")
    remove(f'info/json/{user_id}.json')
    os = workouts["data"]["operating_systems"]
    oss, times = [], []

    for i in os:
        times.append(i["total_seconds"])
        oss.append(i["name"])

    fig, ax = plt.subplots()
    ax.pie(times, labels=oss, shadow=True)
    ax.axis("equal")
    plt.savefig(f"info/images/{user_id}_os_stats")

    img = open(f'info/images/{user_id}_os_stats.png', "rb")
    return img


async def editors_stats(user_id, email, password):

    await record(f"info/json/{user_id}.json", email, password)

    workouts = pd.read_json(f"info/json/{user_id}.json")
    remove(f'info/json/{user_id}.json')
    edit = workouts["data"]["editors"]
    editors, times = [], []

    for i in edit:
        times.append(i["total_seconds"])
        editors.append(i["name"])

    fig, ax = plt.subplots()
    ax.pie(times, labels=editors, shadow=True)
    ax.axis("equal")
    plt.savefig(f"info/images/{user_id}_editors_stats")

    img = open(f'info/images/{user_id}_editors_stats.png', "rb")
    return img


async def categories_stats(user_id, email, password):

    await record(f"info/json/{user_id}.json", email, password)

    workouts = pd.read_json(f"info/json/{user_id}.json")
    remove(f'info/json/{user_id}.json')
    categor = workouts["data"]["categories"]
    categories, times = [], []

    for i in categor:
        times.append(i["total_seconds"])
        categories.append(i["name"])

    fig, ax = plt.subplots()
    ax.pie(times, labels=categories, shadow=True)
    ax.axis("equal")
    plt.savefig(f"info/images/{user_id}_categories_stats")

    img = open(f'info/images/{user_id}_categories_stats.png', "rb")
    return img


async def all_time(user_id, email, password):

    await record(f"info/json/{user_id}.json", email, password)

    workouts = pd.read_json(f"info/json/{user_id}.json")
    remove(f'info/json/{user_id}.json')
    return workouts["data"]["human_readable_total_including_other_language"]
