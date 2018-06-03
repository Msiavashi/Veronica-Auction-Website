# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class PaymentStatus:
    PAID = 1
    UNPAID = 0
    ERROR = -1

class Payment(Base):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    GUID = db.Column(db.String(length=50))
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    status = db.Column(db.Integer,default=1,nullable=False)
    details = db.Column(db.Text)

    payment_method_id = db.Column(db.BigInteger,db.ForeignKey('payment_methods.id'),nullable=False)
    payment_method = db.relationship('PaymentMethod')
    # orders = db.relationship('Order' , secondary = 'payment_orders', back_populates='payments')

    ref_id = db.Column(db.Text)
    sale_order_id = db.Column(db.Integer)
    sale_refrence_id = db.Column(db.Integer)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    # shipment = db.relationship('Shipment')

    messages = db.relationship('PaymentMessage' , secondary = 'payment_message_payments', back_populates='payments')


    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " پرداخت به کد رهگیری : "+ str(self.GUID) + " باوضعیت  :" + str(self.status) + " در تاریخ : " + str(self.created_at)

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Str()
    GUID = fields.Str()
    status = fields.Int()
    created_at = fields.Str()
    details = fields.Raw()
    payment_method = fields.Nested('PaymentMethodSchema')
    # user = fields.Nested('UserSchema',exclude=('payments',))
    # shipment = fields.Nested('ShipmentSchema',exclude=('payment',))
    messages = fields.Nested('PaymentMessageSchema',many=True,exclude=('payments',))
