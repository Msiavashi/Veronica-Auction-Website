from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Role(Base):
    __tablename__ = 'roles'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text,nullable=False)

    users = db.relationship('User' , secondary = 'user_roles', back_populates='roles')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
     updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.name

    def __get__(self,name):
        role = self.query.filter_by(name=name).first()
        return role

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    users = fields.Nested('UserSchema',many=True,exclude=('roles',))
