# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = (db.UniqueConstraint('postal_code', name='address_postal_code_uc'),)

    id = db.Column(db.BigInteger, primary_key=True)
    user = db.relationship('User', uselist=False, back_populates='address')
    # user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    country = db.Column(db.String(length=50),nullable=False,default="ایران")
    state = db.Column(db.String(length=50), nullable=False)
    city = db.Column(db.String(length=50), nullable=False)
    address = db.Column(db.String(length=255), nullable=False)
    postal_code = db.Column(db.String(length=20), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " آدرس :" + self.country + " - " + self.state + "  - " + self.city + " - " + self.address

class AddressSchema(Schema):
    id = fields.Str()
    country = fields.Str()
    state = fields.Str()
    city = fields.Str()
    address = fields.Str()
    postal_code = fields.Str()
