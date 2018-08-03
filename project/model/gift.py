from project.database import db, Base
from marshmallow import Schema, fields
import datetime


class Gift(Base):
    __tablename__ = 'gifts'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    expired = db.Column(db.Boolean,default=False)

    users = db.relationship('User', secondary='user_gifts', back_populates='gifts')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title

class GiftSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    amount = fields.Str()
    users = fields.Nested('UserSchema', many=True,exclude=('gifts',))
