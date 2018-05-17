from project.database import db, Base
from marshmallow import Schema, fields
import datetime

order_items = db.Table('order_items', Base.metadata,
    db.Column('order_id', db.ForeignKey('orders.id')),
    db.Column('item_id', db.ForeignKey('items.id'))
)
