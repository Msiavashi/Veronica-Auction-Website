# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class PaymentMessage(Base):
    __tablename__ = 'payment_messages'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    payments = db.relationship('Payment' , secondary = 'payment_message_payments', back_populates='messages')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title

class PaymentMessageSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    message = fields.Str()
    payments = fields.Nested('PaymentSchema',many=True,exclude=('messages',))
