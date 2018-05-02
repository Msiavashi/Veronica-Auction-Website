from project.database import db, Base
from user_role import user_roles
from marshmallow import Schema, fields

class Role(Base):
    __tablename__ = 'roles'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512))
    users = db.relationship('User', secondary=user_roles,back_populates='roles')

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    users = fields.Nested('UserSchema',many=True)
