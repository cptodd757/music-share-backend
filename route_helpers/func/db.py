import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client["music_share"]
users = db["users"]

def find_one(query):
    return users.find_one(query)

def insert_one(query):
    return users.insert_one(query)

