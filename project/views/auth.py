from http import HTTPStatus

from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.dao.models import User
from project.services import UserService
from project.setup_db import db
from project.tools.validators import AuthValidator
from project.tools.token_generates import Authentication
from project.tools.validators import TokensValidator

auth_ns = Namespace("auth")


@auth_ns.route("/login")
class AuthViewLogin(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            tokens = Authentication().create(**data)
            return tokens, HTTPStatus.CREATED
        except ValidationError as e:
            abort(code=HTTPStatus.BAD_REQUEST, message=str(e))

    def put(self):
        auth = TokensValidator().load(request.json)
        try:
            return Authentication().update(auth), 201
        except ValidationError as e:
            abort(HTTPStatus.BAD_REQUEST, message=str(e))


@auth_ns.route("/register")
class AuthViewRegister(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            return UserService(db.session).create(**data), 201
        except ValidationError:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message="Не могу создать, чего-то не хватает"
            )
