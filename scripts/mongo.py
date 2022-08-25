import pymongo


class Database:
    def __init__(self, connstring):
        """Инициализация подключения к базе данных"""
        self.__connection = pymongo.MongoClient(connstring)
        self.dbUser = self.__connection["test"]
        self.collUser = self.dbUser["users"]

    async def userAdd(self, user_id, email, password):
        """ "Добавление пользователя"""
        self.collUser.insert_one({"_id": user_id, "email": email, "password": password})

    async def userExsist(self, user_id):
        """Проверка наличия пользователя"""
        return self.collUser.find_one({"_id": user_id})

    async def userInfo(self, user_id):
        """Получение информации о пользователе"""
        return self.collUser.find_one({"_id": user_id})

    async def AllUser(self):
        """Получение всех пользователей"""
        return self.collUser.find()
