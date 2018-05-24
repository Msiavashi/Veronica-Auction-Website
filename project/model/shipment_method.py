# -*- coding: utf-8 -*-
import sys
from importlib import reload
reload(sys)
# sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class ShipmentMethod(Base):
    __tablename__ = 'shipment_methods'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), default=0)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title

class ShipmentMethodSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    desciption = fields.Str()
    price = fields.Str()
