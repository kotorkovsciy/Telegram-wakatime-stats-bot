import pymongo


class Database:
    def __init__(self, connstring):
        self.__connection = pymongo.MongoClient(connstring)
        self.dbUser = self.__connection["test"]
        self.collUser = self.dbUser["users"]

    async def userAdd(self, user_id, email, password):
        self.collUser.insert_one(
            {"_id": user_id, "email": email, "password": password})

    async def userExsist(self, user_id):
        return self.collUser.find_one({"_id": user_id})

    async def userInfo(self, user_id):
        return self.collUser.find_one({"_id": user_id})

    async def AllUser(self):
        return self.collUser.find()
