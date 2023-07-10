import pymongo
from pymongo import DESCENDING


class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        Database.__instance = None

    def __init__(self, connstring):
        """Инициализация подключения к базе данных"""
        self.__connection = pymongo.MongoClient(connstring)
        self.__dbUser = self.__connection["test"]
        self.__collUser = self.__dbUser["users"]
        self.__collStats = self.__dbUser["stats"]

    async def userAdd(self, user_id, refresh_token):
        """ "Добавление пользователя"""
        self.__collUser.insert_one({"_id": user_id, "refresh_token": refresh_token})

    async def userExsist(self, user_id):
        """Проверка наличия пользователя"""
        return self.__collUser.find_one({"_id": user_id})

    async def userDel(self, user_id):
        """Удаление пользователя"""
        self.__collUser.delete_one({"_id": user_id})

    async def userInfo(self, user_id):
        """Получение информации о пользователе"""
        return self.__collUser.find_one({"_id": user_id})

    async def AllUser(self):
        """Получение всех пользователей"""
        return self.__collUser.find()

    async def add_stats(self, user_id, date, stats, theme):
        """Добавление статистики"""
        _id = self.__collStats.find().sort("_id", DESCENDING).limit(1)

        if self.__collStats.count_documents({}) == 0:
            _id = 0
        else:
            _id = _id[0]["_id"] + 1

        self.__collStats.insert_one(
            {
                "_id": _id,
                "user_id": user_id,
                "date": date,
                "stats": stats,
                "theme": theme
            }
        )

    async def get_stats(self, user_id, theme):
        """Получение статистики"""
        return self.__collStats.find({"user_id": user_id, "theme": theme})
