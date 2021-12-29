from marshmallow import Schema, fields


class AuthValidator(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)