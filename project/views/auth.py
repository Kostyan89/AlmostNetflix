from http import HTTPStatus

from flask import request
from flask_restx import Resource, Namespace, abort
from marshmallow import ValidationError

from project.dao.models.auth import AuthValidator
from project.implemented import auth_service


auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        try:
            data = AuthValidator().load(request.json)
            tokens = auth_service.create(**data)
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
        tokens = auth_service.update(request.json)
        return tokens, 201