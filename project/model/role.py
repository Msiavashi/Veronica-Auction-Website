from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Role(Base):
    __tablename__ = 'roles'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.name

class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    user = fields.Nested('UserSchema',exclude=('roles',))
