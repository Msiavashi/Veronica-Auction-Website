from project.database import db, Base
from marshmallow import Schema, fields
import datetime

user_gifts = db.Table('user_gifts', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('gift_id', db.ForeignKey('gifts.id')),
    db.Column('used',db.Boolean,default=False)
)

# class user_gift(Base):
#     __tablename__ = 'user_gifts'
#     user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
#     gift_id = db.Column(db.BigInteger, db.ForeignKey('gifts.id'), primary_key=True)
#     used = db.Column(db.Boolean,default=False)
