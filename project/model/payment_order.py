from project.database import db, Base
from marshmallow import Schema, fields
import datetime

payment_orders = db.Table('payment_orders', Base.metadata,
    db.Column('payment_id', db.ForeignKey('payments.id')),
    db.Column('order_id', db.ForeignKey('orders.id'))
)
