import pymongo


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
