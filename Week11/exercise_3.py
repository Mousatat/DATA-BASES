from unittest import result
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client['mydatabase']

collection = db["mydatabse"]

query = {"$and"[{"address": "/.*Rogers Avenue*./"}, "grade":"C"]}

results = collection.find(query)

if results.count() > 1:
    deleted = collection.delete_many(query)
else:
    results.upsert().update({'$push':{'grade':"C"}})
