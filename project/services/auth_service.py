
import calendar

from datetime import datetime, timedelta

from flask import request, current_app
from flask_restx import abort
import jwt

from project.dao.models import User
from project.services.base import BaseService
from project.setup_db import db
from project.config import BaseConfig
from project.tools.security import compare_passwords

algo = 'HS256'


class AuthService(BaseService):
    @staticmethod
    def _generate_tokens(data):
        min = datetime.datetime.utcnow() + timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
        data["exp"] = calendar.timegm(min.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=current_app.config["ALGO"])

        days = datetime.datetime.utcnow() + timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
        data["exp"] = calendar.timegm(days.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=current_app.config["ALGO"])
        return {"access_token": access_token, "refresh_token": refresh_token}

    def create(self, username, password):
        user = db.session.query(User).filter(User.username == username).first()

        ok = compare_passwords(password_hash=user.password, other_password=password)
        if not ok:
            abort(401)
        return self._generate_tokens({
            "email": user.email,
            "role": user.role
        })

    def update(self, _generate_tokens):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")

        user = db.session.query(User).filter(User.username == username).first()
        tokens = _generate_tokens(data)

        return tokens, 201
