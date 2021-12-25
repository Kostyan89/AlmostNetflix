from http import HTTPStatus

from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.dao.models import User
from project.dao.models.auth import AuthValidator
from project.schemas.users import UserSchema
from project.services.auth_service import AuthService
from project.setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthViewLogin(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            tokens = AuthService().create(**data)
            return tokens, HTTPStatus.CREATED
        except ValidationError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )

    def put(self):
        auth = AuthValidator().load(request.json)
        if auth is None:
            abort(400)
        tokens = AuthService().update(request.json)
        return tokens, 201


@auth_ns.route('/register')
class AuthViewRegister(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            new_user = User(**data)
            return new_user, 201
        except ValidationError:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message="Не могу создать, чего-то не хватает"
            )