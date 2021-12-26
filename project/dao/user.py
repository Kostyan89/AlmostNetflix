import base64
import hashlib
import hmac

from flask_restx import abort

from project.dao.base import BaseDAO
from project.dao.models import User, user
from project.config import BaseConfig


class UserDAO(BaseDAO):
    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        new_user = User(**user_d)
        data_for_check = User.get_by_email(user_d.email)
        if user_d["email"] == data_for_check:
            abort(405)
        self.session.add(new_user)
        self.session.commit()
        return user

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            BaseConfig.PWD_HASH_SALT,
            BaseConfig.PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def compare_passwords(self, get_hash, password):
        return hmac.compare_digest(
            base64.b64decode(get_hash),
            hashlib.pbkdf2_hmac('sha256', password.encode(), BaseConfig.PWD_HASH_SALT, BaseConfig.PWD_HASH_ITERATIONS))

    def partially_update(self, user_d):
        user = self.get_by_id(user_d.get("id"))
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")
        user.favorite_genre = user_d.get("favorite_genre")
        self.session.add(user)
        self.session.commit()

    def update(self, new_password):
        user.password = new_password
        self.session.add(user)
        self.session.commit()

