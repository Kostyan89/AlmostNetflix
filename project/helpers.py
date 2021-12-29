import jwt
from flask import request
from flask_restx import abort

from project.config import BaseConfig


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split["Bearer "][-1]
        try:
            user = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            print("JWT Decode Exception", e)
        return func(*args, *kwargs, uid=user['id'])
    return wrapper