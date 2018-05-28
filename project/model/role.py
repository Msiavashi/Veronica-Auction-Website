from project.database import db, Base
from marshmallow import Schema, fields
import datetime
from flask_login import RoleMixin

class Role(Base,RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text,nullable=False)

    users = db.relationship('User' , secondary = 'user_roles', back_populates='roles' )

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.name

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    users = fields.Nested('UserSchema',many=True,exclude=('roles',))
