# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title

class PaymentMethodSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    desciption = fields.Str()
    details = fields.Str()
