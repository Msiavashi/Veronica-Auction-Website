from project.database import db, Base
from marshmallow import Schema, fields
import datetime

user_roles = db.Table('user_roles', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('role_id', db.ForeignKey('roles.id'))
)
