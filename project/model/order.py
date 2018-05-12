from project.database import db, Base
import datetime
from marshmallow import Schema, fields
from .order_item import order_items

class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.BigInteger, primary_key=True)
    create_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    status = db.Column(db.Boolean)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    items = db.relationship('Item', secondary = 'order_items', back_populates='orders')
    shipment_id = db.Column(db.BigInteger, db.ForeignKey('shipments.id'))
    shipment = db.relationship('Shipment')
    def __str__(self):
        return str(self)

class OrderSchema(Schema):
    id = fields.Int()
    create_at = fields.DateTime()
    updated_at = fields.DateTime()
    status = fields.Boolean()
    user = fields.Nested('UserSchema')
    items = fields.Nested('ItemSchema',many=True,exclude=('orders',))
    shipment = fields.Nested('ShipmentSchema',exclude=('order',))
