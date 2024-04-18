import pymongo
from pymongo import DESCENDING
from os import getenv

class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        Database.__instance = None

    def __init__(self, connstring: str) -> None:
        """Init database

        Args:
            connstring (str): Connection string
        """
        self.__connection = pymongo.MongoClient(connstring)
        self.__db_user = self.__connection[getenv("DB_NAME")]
        self.__coll_user = self.__db_user["users"]
        self.__coll_stats = self.__db_user["stats"]

    async def user_add(self, user_id: int, refresh_token: str, access_token: str) -> None:
        """Create user

        Args:
            user_id (int): User id
            refresh_token (str): Refresh token
        """
        self.__coll_user.insert_one({"_id": user_id, "refresh_token": refresh_token, "access_token": access_token })

    async def user_update(self, user_id: int, refresh_token: str, access_token: str) -> None:
        """Update user

        Args:
            user_id (int): User id
            refresh_token (str): Refresh token
        """
        self.__coll_user.update_one(
            {"_id": user_id}, {"$set": {"refresh_token": refresh_token, "access_token": access_token }}
        )

    async def user_exsist(self, user_id: int) -> bool:
        """Check user

        Args:
            user_id (int): User id

        Returns:
            bool: User exsist
        """
        return self.__coll_user.find_one({"_id": user_id})

    async def user_del(self, user_id: int) -> None:
        """Delete user

        Args:
            user_id (int): User id
        """
        self.__coll_user.delete_one({"_id": user_id})

    async def user_info(self, user_id: int) -> dict:
        """Get user info

        Args:
            user_id (int): User id

        Returns:
            dict: User info
        """
        return self.__coll_user.find_one({"_id": user_id})

    async def all_user(self) -> list[dict]:
        """Get all users

        Returns:
            list[dict]: All users
        """
        return self.__coll_user.find()

    async def add_stats(self, user_id: int, date: str, stats: dict, theme: str) -> None:
        """Write statistics

        Args:
            user_id (int): User id
            date (str): Date
            stats (dict): Statistics
            theme (str): Theme
        """
        _id = self.__coll_stats.find().sort("_id", DESCENDING).limit(1)

        if self.__coll_stats.count_documents({}) == 0:
            _id = 0
        else:
            _id = _id[0]["_id"] + 1

        self.__coll_stats.insert_one(
            {
                "_id": _id,
                "user_id": user_id,
                "date": date,
                "stats": stats,
                "theme": theme,
            }
        )

    async def get_stats(self, user_id: int, theme: str) -> list[dict]:
        """Get statistics

        Args:
            user_id (int): User id
            theme (str): Theme

        Returns:
            list[dict]: Statistics
        """
        return self.__coll_stats.find({"user_id": user_id, "theme": theme})
