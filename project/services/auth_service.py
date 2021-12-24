import base64
import calendar
import hashlib
import hmac
from datetime import datetime, timedelta

from flask import request
from flask_restx import abort
from jwt import jwt

from project.dao.models import User
from project.implemented import users_service
from project.setup_db import db
from project.config import BaseConfig


algo = 'HS256'


class AuthService:
    @staticmethod
    def _generate_tokens(data):
        now = datetime.now()

        min = now + timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data["exp"] = calendar.timegm(min.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)

        days = now + timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data["exp"] = calendar.timegm(days.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def create(self, username, password):
        user = db.session.query(User).filter(User.username == username).first()

        ok = users_service.compare_passwords(password_hash=user.password, other_password=password)
        if not ok:
            abort(401)
        return self._generate_tokens({
            "username": user.username,
            "role": user.role
        })

    def update(self):
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

        data = {
            "username": user.username,
            "role": user.role
        }
        min = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data["exp"] = calendar.timegm(min.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)
        days = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data["exp"] = calendar.timegm(days.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201