
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")


db = client['mydatabase']

collection = db["mydatabse"]

first = collection.find({"cuisine":"Indian"})
second = collection.find({"$or":[{"cuisine":"Indian"}, {"cousine":"Thai"}]})
third = collection.find({"address": "/1115 Rogers Avenue, 11226*./"})



