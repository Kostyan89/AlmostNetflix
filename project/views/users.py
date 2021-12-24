from http import HTTPStatus

from flask_restx import Resource, Namespace, ValidationError, abort
from flask import request

from helpers import auth_required
from project.implemented import users_service, user_schema, user_dao
from project.dao.models import User
from project.setup_db import db

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def post(self):
        try:
            data = user_dao.load(request.json)
            new_user = users_service.create_user(**data)
            return user_schema.dump(new_user), 201
        except ValidationError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )


@users_ns.route('<uid: int>')
class UserService(Resource):
    @auth_required
    def get(self, uid):
        user = users_service.get_one(uid)
        selected_user = user_schema.dump(user)
        return selected_user, 200

    @auth_required
    def put(self, uid):
        updated_user = users_service.filter_by(uid).update(request.json)
        return user_schema.dump(updated_user), 204

    @auth_required
    def patch(self, uid):
        user = users_service.filter_by(uid).partially_update(request.json)
        return user, 204
