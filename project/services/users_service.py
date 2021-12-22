from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.users import UserSchema
from project.services.base import BaseService


class UsersService(BaseService):
    def get_item_by_id(self, uid):
        user = UserDAO(self._db_session).get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)
