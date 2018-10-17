# -*- coding: utf-8 -*-
import sys
reload(sys)
import random
sys.setdefaultencoding("utf-8")
from project.database import db, Base
from marshmallow import Schema, fields
from datetime import datetime
import time

class PaymentStatus:
    PAID = 100
    BANK = 200
    PAYING = 300
    ERROR = 400
    ABORT = 500
    UNPAID = 0

class PaymentType:
    NOTITLE = 0
    PLAN = 1000
    WALET = 2000
    PRODUCT = 3000
    FREE = 4000

class Payment(Base):
    random.seed(time.time())
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    GUID = db.Column(db.String(64) ,default = random.randint(100000000000,10000000000000000) , onupdate=random.randint(100000000000,10000000000000000))
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    status = db.Column(db.Integer,default=PaymentStatus.UNPAID,nullable=False)
    type = db.Column(db.String(64),default=PaymentType.NOTITLE)
    details = db.Column(db.Text)

    payment_method_id = db.Column(db.BigInteger,db.ForeignKey('payment_methods.id'),nullable=False)
    payment_method = db.relationship('PaymentMethod')
    # orders = db.relationship('Order' , secondary = 'payment_orders', back_populates='payments')

    ref_id = db.Column(db.Text)
    sale_order_id = db.Column(db.String(255))
    sale_refrence_id = db.Column(db.String(255))

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    # shipment = db.relationship('Shipment')

    messages = db.relationship('PaymentMessage' , secondary = 'payment_message_payments', back_populates='payments')


    created_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False ,onupdate=datetime.now)

    def __str__(self):
        return " پرداخت به کد رهگیری : "+ str(self.GUID) + " باوضعیت  :" + str(self.status) + " در تاریخ : " + str(self.created_at)

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Str()
    GUID = fields.Str()
    status = fields.Int()
    type = fields.Str()
    created_at = fields.Str()
    details = fields.Raw()
    ref_id = fields.Str()
    sale_refrence_id = fields.Str()
    payment_method = fields.Nested('PaymentMethodSchema')
    # user = fields.Nested('UserSchema',exclude=('payments',))
    # shipment = fields.Nested('ShipmentSchema',exclude=('payment',))
    messages = fields.Nested('PaymentMessageSchema',many=True,exclude=('payments',))
