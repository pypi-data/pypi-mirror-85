"""
Apartment related services used to perform complex interactions with database.
"""
from .schemas import ApartmentSchema
from ...addons import db
from ...coreutils.service import BaseService
from ..bookmark.services import BookmarkService


class ApartmentService(BaseService):
    """
    Basic apartment service with actions: get, create, update, delete.
    """
    @classmethod
    def search(cls):
        return BaseService.search(db.apartments)

    @classmethod
    def validate(cls, data, schema):
        return BaseService.validate(data, schema=schema)

    @classmethod
    def create(cls, data, schema=ApartmentSchema()):
        return BaseService.create(db.apartments, data, schema=schema)

    @classmethod
    def update(cls, uid, data):
        return BaseService.update(db.apartments, uid, data)

    @classmethod
    def get_details(cls, uid):
        bookmarks = BookmarkService.search({'apartment_id': uid})
        apartment = BaseService.get_details(db.apartments, uid)
        apartment['bookmarks'] = bookmarks
        return apartment

    @classmethod
    def delete(cls, uid):
        return BaseService.delete(db.apartments, uid)
