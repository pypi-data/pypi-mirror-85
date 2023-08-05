import bson
from marshmallow.exceptions import ValidationError
from .exceptions import APIError


class BaseService:
    @classmethod
    def object_id(cls, uid):
        """
        Return object id for the given uid string and handle deserialization error
        """
        try:
            return bson.ObjectId(uid)
        except bson.errors.InvalidId:
            raise APIError('{} is not a valid bson.ObjectId'.format(uid))

    @classmethod
    def search(cls, collection, filters={}):
        apartments = [apartment for apartment in collection.find(filters)]
        return apartments

    @classmethod
    def get_details(cls, collection, uid):
        print(collection.name)
        result = collection.find_one({'_id': cls.object_id(uid)})
        if result is None:
            raise APIError(
                "No object matching _id '{}' in collection '{}'".format(uid, collection.name), status=404)
        return result

    @classmethod
    def validate(cls, data, schema=None):
        if data is None:
            raise APIError("Data of the apartment to be created must be passed a json body", status=400)
        
        try:
            if schema is None:
                return data
            else:
                return schema.load(data)
        except ValidationError as error:
            raise APIError("Error validating input data", causes=error.messages)

    @classmethod
    def create(cls, collection, data, schema=None):
        validated = cls.validate(data, schema=schema)
        result = collection.insert_one(validated)
        return collection.find_one({'_id': result.inserted_id})

    @classmethod
    def update(cls, collection, uid, data):
        validated = cls.validate(data)
        validated.pop('_id', None) # remove field "_id" if set
        object_uid = cls.object_id(uid)
        result = collection.update_one({'_id': object_uid}, {"$set": validated}, upsert=True)
        return collection.find_one({'_id': object_uid})

    @classmethod
    def delete(cls, collection, uid):
        result = collection.remove({'_id': cls.object_id(uid)})
        return result
