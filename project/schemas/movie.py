from datetime import datetime

from marshmallow import fields, Schema
from marshmallow.validate import Range


class MovieSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True, validate=Range(min=0, max=datetime.now().year))
    rating = fields.Float(required=True, validate=Range(min=0, max=10))
    genre_id = fields.Int(required=True)
    director_id = fields.Int(required=True)

    