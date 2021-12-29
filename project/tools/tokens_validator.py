from marshmallow import fields, Schema


class TokensValidator(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str(required=True)