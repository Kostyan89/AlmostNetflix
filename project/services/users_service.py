from sqlalchemy.orm.scoping import scoped_session

from project.dao.user import UserDAO
from project.exceptions import ItemNotFound, DublicateError
from project.schemas.users import UserSchema
from project.services.base import BaseService
from project.setup_db import db

from project.tools.security import get_hash, compare_passwords, generate_password_digest


class UserService(BaseService):

    def get_item_by_id(self, uid):
        user = UserDAO(db.session).get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(db.session).get_all()
        return UserSchema(many=True).dump(users)

    def partially_update(self, uid, **kwargs):
        return UserDAO(db.session).partially_update(uid, **kwargs)

    def update_password(self, uid, new_password):
        user = self.get_item_by_id(uid)
        password_hash = get_hash(new_password)
        compare_passwords(password_hash, user.password)
        UserDAO(db.session).update(password_hash)
        return user

    def create(self, **data_in):
        try:
            user_pass = data_in.get("password")
            if user_pass:
                data_in["password"] = generate_password_digest(user_pass)
            user = UserDAO(self._db_session).create(**data_in)
            return UserSchema().dump(user)
        except Exception:
            DublicateError
