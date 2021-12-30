from marshmallow import fields, Schema


class UserData(Schema):
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()


class UserSchema(UserData):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

