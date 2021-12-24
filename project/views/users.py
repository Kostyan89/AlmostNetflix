from flask_restx import Resource, Namespace
from flask import request

from project.dao.models import User
from project.setup_db import db

users_ns = Namespace('users')


@users_ns.route('/user')
class UsersView(Resource):
    def post(self):
        req_json = request.json
        new_user = user_service.create(req_json)
        return user_schema.dump(new_user), 201

