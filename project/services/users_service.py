import base64
import hashlib
import hmac

from project.dao.models import User
from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.users import UserSchema
from project.services.base import BaseService
from project.config import BaseConfig

class UserService(BaseService):
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_item_by_id(self, uid):
        user = UserDAO(self._db_session).get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create_user(self, user_d):
        return self.dao.create(user_d)

    def partially_update(self, uid):
        user = self.get_item_by_id(uid)
        if "name" in user:
            user.name = user.get("name")
        if "surname" in user:
            user.surname = user.get("surname")
        if "favorite_genre" in user:
            user.surname = user.get("favorite_genre")
        self.dao.partially_update(user)

    def update_password(self, uid, password, new_password):
        user = self.get_item_by_id(uid)
        if password in user:
            user.password = user.get(new_password)
        self.dao.update(user)
