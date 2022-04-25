from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")


db = client['mydatabase']

collection = db["mydatabse"]

first = collection.delete_one({"borough":"Manhattan"})
second = collection.delete_many({"cuisine":"Thai"})
