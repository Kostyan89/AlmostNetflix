from project.dao.base import BaseDAO
from project.dao.models import Genre


class GenreDAO(BaseDAO):
    def get_by_id(self, pk):
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(Genre).all()
