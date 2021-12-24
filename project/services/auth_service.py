import base64
import calendar
import hashlib
import hmac
from datetime import datetime, timedelta

from flask import request
from flask_restx import abort
from jwt import jwt

from project.dao.models import User
from project.implemented import user_service
from project.setup_db import db


secret = 's3cR$eT'
algo = 'HS256'


class AuthService:
    @staticmethod
    def _generate_tokens(data):
        now = datetime.now()

        min30 = now + timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)

        days130 = now + timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def create(self, username, password):
        user = db.session.query(User).filter(User.username == username).first()

        ok = user_service.compare_passwords(password_hash=user.password, other_password=password)
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
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")

        user = db.session.query(User).filter(User.username == username).first()

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201