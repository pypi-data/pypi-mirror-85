"""
Load environment variables from shell context or set it to default values.
"""
from os import getenv as _getenv

MONGO_DATABASE_URI = _getenv('MONGO_DATABASE_URI', 'mongodb://admin:admin@localhost:27017')
