from marshmallow import Schema, fields

from project.dao.models.base import BaseMixin
from project.setup_db import db


class Auth(BaseMixin, db.Model):
    __tablename__ = 'auth'
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))




