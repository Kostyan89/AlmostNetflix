from marshmallow import fields, Schema


class TokensValidator(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str(required=True)


class AuthValidator(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)