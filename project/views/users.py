from http import HTTPStatus

from flask_restx import Resource, Namespace, ValidationError, abort
from flask import request
from project.implemented import users_service, user_schema
from project.dao.models import User
from project.setup_db import db

users_ns = Namespace('users')


@users_ns.route('/user')
class UsersView(Resource):
    def post(self):
        try:
            data = User().load(request.json)
            new_user = users_service.create_user(**data)
            return user_schema.dump(new_user), 201
        except ValidationError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )


