import base64
import hashlib
import hmac
from sqlite3 import IntegrityError

from flask_restx import abort

from project.dao.base import BaseDAO
from project.dao.models import User, user
from project.config import BaseConfig
from project.exceptions import ItemNotFound, DublicateError


class UserDAO(BaseDAO):
    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, email, password):
        try:
            new_user = User(email, password)
            self._db_session.add(new_user)
            self._db_session.commit()
            return new_user
        except IntegrityError as e:
            raise DublicateError

    def partially_update(self, user_d, name=None, surname=None, favorite_genre=None):
        user = self.get_by_id(user_d)
        if name:
            user.name = name
        self._db_session.add(user)
        self._db_session.commit()

    def update(self, user_id, new_password):
        self.get_by_id(user_id)
        user.password = new_password
        self._db_session.add(user)
        self._db_session.commit()

