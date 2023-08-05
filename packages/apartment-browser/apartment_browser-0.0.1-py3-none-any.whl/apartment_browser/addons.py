"""
Definition of app addons that will be used in various places.
"""
from pymongo import MongoClient
from .settings import MONGO_DATABASE_URI


mongo = MongoClient(MONGO_DATABASE_URI)
db = mongo.apartment
