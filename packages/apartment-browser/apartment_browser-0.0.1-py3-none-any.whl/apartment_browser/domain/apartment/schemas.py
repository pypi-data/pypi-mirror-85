"""
Schemas used to validate apartment structure on input.
"""
from marshmallow import fields, Schema
from ..commons.schemas import PlaceSchema

class ApartmentSchema(Schema):
    """
    Default apartment schema.
    """
    prix = fields.Integer(required=True)
    pieces = fields.Integer(required=True)
    place = fields.Nested(PlaceSchema, required=True)
