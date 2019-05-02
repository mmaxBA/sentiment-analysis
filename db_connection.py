import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

def connect():
    client = MongoClient('localhost', 27017)
    db = client.sentiment
    collection = db.sentiment
    return collection
