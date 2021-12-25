from http import HTTPStatus

from flask_restx import Resource, Namespace, ValidationError, abort
from flask import request

from project.helpers import auth_required
from project.schemas.users import UserSchema
from project.services import UserService
from project.setup_db import db

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    def post(self):
        try:
            data = UserSchema().load(request.json)
            return UserService(db.session).create_user(**data)
        except ValidationError as e:
            abort(
                code=HTTPStatus.BAD_REQUEST,
                message=str(e)
            )


@users_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        user = UserService(db.session).get_item_by_id(uid)
        selected_user = UserSchema().dump(user)
        return selected_user, 200

    @auth_required
    def patch(self, uid):
        user = UserService(db.session).filter_by(uid).partially_update(request.json)
        return user, 204


# @users_ns.route('/password')
# class UserView2(Resource):
#     @auth_required
#     def put(self, uid, new_password):
#         user = UserService.get_item_by_id(uid)
#
#
#         return UserSchema.dump(updated_user), 204