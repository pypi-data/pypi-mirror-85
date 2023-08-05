from marshmallow.exceptions import ValidationError
from bson import ObjectId
from .schemas import BookmarkSchema
from ...addons import db
from ...coreutils.exceptions import APIError
from ...coreutils.service import BaseService


class BookmarkService(BaseService):
    @classmethod
    def search(cls, filters={}):
        return BaseService.search(db.bookmarks, filters=filters)

    @classmethod
    def validate(cls, data, schema):
        return BaseService.validate(data, schema=schema)

    @classmethod
    def create(cls, data, schema=BookmarkSchema()):
        # validate bookmark schema
        validated = BaseService.validate(data, schema=schema)
        # try to get apartment to check it exists
        BaseService.get_details(db.apartments, validated['apartment_id'])
        # if it exists allow the creation of this bookmark
        return BaseService.create(db.bookmarks, data, schema=schema)

    @classmethod
    def update(cls, uid, data):
        return BaseService.update(db.bookmarks, uid, data)

    @classmethod
    def get_details(cls, uid):
        return BaseService.get_details(db.bookmarks, uid)

    @classmethod
    def delete(cls, uid):
        return BaseService.delete(db.bookmarks, uid)
