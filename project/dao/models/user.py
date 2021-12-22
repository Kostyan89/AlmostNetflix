from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User '{self.name.title()}'>"