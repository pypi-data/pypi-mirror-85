import pymongo


class Mongo:
    def __init__(self, url: str, database: str):
        self.connection = pymongo.MongoClient(url)
        self.database = self.connection[database]