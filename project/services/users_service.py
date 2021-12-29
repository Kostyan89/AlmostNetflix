from sqlalchemy.orm.scoping import scoped_session

from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.users import UserSchema
from project.services.base import BaseService

from project.tools.security import get_hash, compare_passwords


class UserService(BaseService):
    def __init__(self, session: scoped_session):
        super().__init__(self, session)
        self.dao = UserDAO(self._db_session)

    def get_item_by_id(self, uid):
        user = self.dao.get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = self.dao.get_all()
        return UserSchema(many=True).dump(users)

    def create_user(self, user_d):
        return self.dao.create(user_d)

    def partially_update(self, uid, **kwargs):
        return self.dao.partially_update(uid, **kwargs)

    def update_password(self, uid, new_password):
        user = self.get_item_by_id(uid)
        password_hash = get_hash(new_password)
        compare_passwords(password_hash, user.password)
        self.dao.update(password_hash)
        return user
