
from sqlite3 import IntegrityError
from project.dao.base import BaseDAO
from project.dao.models import User, user
from project.exceptions import DublicateError


class UserDAO(BaseDAO):
    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, email=None, password=None):
        try:
            user_d = User(email, password)
            self._db_session.add(user_d)
            self._db_session.commit()
            return user_d
        except IntegrityError:
            raise DublicateError

    def partially_update(self, user_d, name=None, surname=None, favorite_genre=None):
        user = self.get_by_id(user_d)
        if name:
            user.name = name
        if surname:
            user.surname = surname
        if favorite_genre:
            user.favorite_genre = favorite_genre
        self._db_session.add(user)
        self._db_session.commit()

    def update(self, user_id, new_password):
        self.get_by_id(user_id)
        user.password = new_password
        self._db_session.add(user)
        self._db_session.commit()
