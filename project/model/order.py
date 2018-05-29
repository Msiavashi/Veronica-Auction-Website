from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.BigInteger, primary_key=True)
    desciption = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    register_user = db.Column(db.Boolean,default=False)
    total_cost = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    items = db.relationship('Item',secondary='order_items',back_populates='orders')

    # payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id','orders.id'))
    # payment = db.relationship('Payment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        res = str(self.user)
        for item in self.items:
            res +=" "+str(item)
        return res

class OrderSchema(Schema):
    id = fields.Int()
    desciption = fields.Str()
    status = fields.Str()
    register_user = fields.Boolean()
    total_cost = fields.Str()
    create_at = fields.DateTime()
    updated_at = fields.DateTime()
    # user = fields.Nested('UserSchema',exclude=('orders',))
    # payment = fields.Nested('PaymentSchema',exclude=('order',))
    items = fields.Nested('ItemSchema',many=True,exclude=('orders',))
