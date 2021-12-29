from http import HTTPStatus

from flask_restx import Resource, Namespace, ValidationError, abort
from flask import request

from project.exceptions import DublicateError, ItemNotFound
from project.helpers import auth_required
from project.schemas.users import UserSchema, UserData
from project.services import UserService
from project.setup_db import db

users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):
    def post(self):
        try:
            data = UserSchema().load(request.json)
            return UserService(db.session).create_user(**data)
        except ValidationError as e:
            abort(code=HTTPStatus.BAD_REQUEST, message=str(e))
        except DublicateError:
            abort(404)


@users_ns.route("/<int:uid>")
class UserView(Resource):
    @auth_required
    def get(self, uid):
        try:
            user = UserService(db.session).get_item_by_id(uid)
            return UserSchema().dump(user), 200
        except ItemNotFound as e:
            abort(code=HTTPStatus.BAD_REQUEST, message=str(e))

    @auth_required
    def patch(self, uid):
        data = UserData().load(request.json)
        try:
            user = UserService(db.session).partially_update(uid, data)
            return user, 204
        except ValueError as e:
            abort(code=404, message=str(e))


@users_ns.route("/password")
class UserView2(Resource):
    @auth_required
    def put(self, uid, new_password):
        try:
            UserService(db.session).update_password(uid, new_password)
            return "", 204
        except ValueError as e:
            abort(code=HTTPStatus.BAD_REQUEST, message=str(e))
