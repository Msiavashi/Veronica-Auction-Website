# -*- coding: utf-8 -*-
import sys
import random
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class ShipmentStatus:
    IN_STORE = 0
    READY_TO_SEND = 1
    SENT = 2
    DELIVERED = 3


class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)

    guid = db.Column(db.String(64), default = random.randint(100000000000,10000000000000000))

    shipment_method_id = db.Column(db.BigInteger,db.ForeignKey('shipment_methods.id'))
    shipment_method = db.relationship('ShipmentMethod')

    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'), nullable=True)      #TODO: remove the nullable later
    insurance = db.relationship('Insurance')

    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    status = db.Column(db.Integer, default=ShipmentStatus.IN_STORE)

    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'))
    order = db.relationship('Order')
    # payment = db.relationship('Payment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        if(self.status):
            status = "ارسال موفقیت آمیز"
        else:
            status = "عدم ارسال موفقیت آمیز"
        return "روش ارسال :" + str(self.shipment_method) + " - تاریخ :" + str(self.send_date) + " - هزینه ارسال :" + str(self.shipment_method.price) + " - وضعیت :" + status

class ShipmentSchema(Schema):
    id = fields.Int()
    guid = fields.Str()
    company = fields.Str()
    method = fields.Str()
    send_date = fields.DateTime()
    recieve_date = fields.DateTime()
    price = fields.Str()
    status = fields.Int()
    # insurance = fields.Nested('InsuranceSchema',exclude=('shipment',))
    payment = fields.Nested('PaymentSchema',exclude=('shipment',))
    order = fields.Nested('OrderSchema',exclude=('shipment',))
