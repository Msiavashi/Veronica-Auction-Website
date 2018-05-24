# -*- coding: utf-8 -*-
import sys
from importlib import reload
reload(sys)
# sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)

    shipment_method_id = db.Column(db.BigInteger,db.ForeignKey('shipment_methods.id'))
    shipment_method = db.relationship('ShipmentMethod')

    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'))
    insurance = db.relationship('Insurance')

    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    status = db.Column(db.Boolean)

    payment_id = db.Column(db.BigInteger, db.ForeignKey('payments.id'))
    payment = db.relationship('Payment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " ارسال توسط :" + str(self.company) + " درتاریخ " + self.send_date + " با قیمت " + self.price + " باوضعیت " + self.status

class ShipmentSchema(Schema):
    id = fields.Int()
    company = fields.Str()
    method = fields.Str()
    send_date = fields.DateTime()
    recieve_date = fields.DateTime()
    price = fields.Str()
    status = fields.Boolean()
    insurance = fields.Nested('InsuranceSchema',exclude=('shipment',))
    payment = fields.Nested('OrderSchema',exclude=('shipment',))
