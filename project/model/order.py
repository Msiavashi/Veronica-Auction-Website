# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields ,post_load
import datetime

# each order has a status for servicing
class OrderStatus:
    UNPAID = 400
    PAYING = 300
    DEACTIVATE = 200
    PAID = 100

class OrderDiscountStatus:
    REGULAR = 0
    INAUCTION = 1
    AUCTIONWINNER = 2
    EXPIRED = 3



class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.BigInteger, primary_key=True)

    desciption = db.Column(db.Text)

    status = db.Column(db.Integer, default=0)
    discount_status = db.Column(db.Integer, default=0)

    total = db.Column(db.Integer,nullable=False)

    total_cost = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    total_discount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item')

    shipmet = db.relationship('Shipment')

    # payments = db.relationship('Payment',secondary='payment_orders',back_populates='orders')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return "کاربر : "+str(self.user) +" - محصول : "+ str(self.item) + " - تعداد : " + str(self.total) + " - جمع کل : " + str(self.total * self.item.price - self.item.discount)

class OrderSchema(Schema):
    id = fields.Int()
    desciption = fields.Str()
    discount_status = fields.Str()
    status = fields.Str()
    register_user = fields.Boolean()
    total = fields.Str()
    total_cost = fields.Str()
    total_discount = fields.Str()
    create_at = fields.DateTime()
    updated_at = fields.DateTime()
    # user = fields.Nested('UserSchema',exclude=('orders',))
    item = fields.Nested('ItemSchema',exclude=('orders',))
    payment = fields.Nested('PaymentSchema')

    @post_load
    def make_order(self,data):
        return Order(**data)
