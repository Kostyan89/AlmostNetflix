from http import HTTPStatus

from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.dao.models import User
from project.tools.validators import AuthValidator
from project.schemas.users import UserSchema
from project.services.auth_service import AuthService
from project.setup_db import db
from project.tools.validators import TokensValidator

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthViewLogin(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            tokens = AuthService(db.session).create(**data)
            return tokens, HTTPStatus.CREATED
        except ValidationError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )

    def put(self):
        auth = TokensValidator().load(request.json)
        if auth is None:
            abort(400)
        tokens = AuthService(db.session).update(request.json)
        return tokens, 201


@auth_ns.route('/register')
class AuthViewRegister(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            return User(**data), 201
        except ValidationError:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message="Не могу создать, чего-то не хватает"
            )