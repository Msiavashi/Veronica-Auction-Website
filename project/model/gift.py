from project.database import db, Base
from marshmallow import Schema, fields


class Gift(Base):
    __tablename__ = 'gifts'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    users = db.relationship('User', secondary='user_gifts', back_populates='gifts')
    def __str__(self):
        return self.name

class GiftSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount = fields.Str()
    users = fields.Nested('UserSchema', many=True,exclude=('gifts',))
