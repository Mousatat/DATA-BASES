


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")


db = client['mydatabase']

collection = db["mydatabse"]


collection.insert_one({"address": "1480 2 Avenue, 10075, -73.9557413, 40.7720266",
                        "borough": "Manhattan",
                        "cuisine": "Italian",
                        "name": "Vella",
                        "id": "41704620",
                        "grades": "A, 11, 01 Oct, 2014"})