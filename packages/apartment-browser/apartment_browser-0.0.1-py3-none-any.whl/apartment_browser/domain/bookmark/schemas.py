"""
Schemas used to validate bookmark structure on input.
"""
from marshmallow import fields, Schema

class BookmarkSchema(Schema):
    url = fields.Url(required=True)
    title = fields.String(required=True)
    apartment_id = fields.String(required=True)
