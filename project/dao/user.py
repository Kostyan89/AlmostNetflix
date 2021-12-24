import base64
import hashlib
import hmac

from flask_restx import abort
from sqlalchemy.orm.scoping import scoped_session

from project.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        data_for_check = User.get_by_email(user_d.email)
        if user_d["email"] == data_for_check:
            abort(405)

        self.session.add(ent)
        self.session.commit()
        return ent

    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def compare_passwords(self, get_hash, password):
        return hmac.compare_digest(
            base64.b64decode(get_hash),
            hashlib.pbkdf2_hmac('sha256', password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS))

