# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)

    shipment_method_id = db.Column(db.BigInteger,db.ForeignKey('shipment_methods.id'))
    shipment_method = db.relationship('ShipmentMethod')

    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'), nullable=True)      #TODO: remove the nullable later
    insurance = db.relationship('Insurance')

    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    status = db.Column(db.String(255), default="ارسال نشده")

    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'))
    # payment = db.relationship('Payment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        if(self.status):
            status = "ارسال موفقیت آمیز"
        else:
            status = "عدم ارسال موفقیت آمیز"
        return "روش ارسال :" + str(self.shipment_method) + " - تاریخ :" + str(self.send_date) + " - هزینه ارسال :" + str(self.shipment_method.price) + " - وضعیت :" + status

class ShipmentSchema(Schema):
    id = fields.Int()
    company = fields.Str()
    method = fields.Str()
    send_date = fields.DateTime()
    recieve_date = fields.DateTime()
    price = fields.Str()
    status = fields.Boolean()
    # insurance = fields.Nested('InsuranceSchema',exclude=('shipment',))
    payment = fields.Nested('OrderSchema',exclude=('shipment',))
