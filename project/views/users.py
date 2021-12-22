from flask_restx import Resource, Namespace
from flask import request

from project.dao.models import User
from project.setup_db import db

users_ns = Namespace('users')


@user_ns.route('/user')
class UsersView(Resource):
    def post(self):
        req_json = request.json
        user = User(**req_json)
        db.session.add(user)
        db.session.commit()
        return "", 201, {"location": f"/movies/{user.id}"}