# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Item(Base):
    __tablename__ = 'items'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text(),nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True, default=0)
    details = db.Column(db.Text())
    images = db.Column(db.Text, nullable=False)

    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')

    orders = db.relationship('Order',secondary='order_items',back_populates='items')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    def __str__(self):
        return  " محصول :"+self.product.title + " آیتم: " + self.title

class ItemSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    desciption = fields.Str()
    price = fields.Int()
    discount = fields.Int()
    details = fields.Str()
    images = fields.Str()

    product = fields.Nested('ProductSchema',exclude=('items',))
    inventories = fields.Nested('InventorySchema', many=True,exclude=('items',))
    insurances = fields.Nested('InsuranceSchema',many=True,exclude=('items',))
    payments = fields.Nested('PaymentSchema',many=True,exclude=('items',))
    orders = fields.Nested('OrderSchema',many=True,exclude=('items',))
