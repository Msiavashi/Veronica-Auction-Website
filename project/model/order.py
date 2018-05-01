from project.database import db, Base
import datetime
from shipment import Shipment
from order_item import order_items

class Order(Base):

    __tablename__ = 'orders'

    id = db.Column(db.BigInteger, primary_key=True)
    create_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    items = db.relationship('Item', secondary = order_items, back_populates='orders')
    shipment_id = db.Column(db.BigInteger, db.ForeignKey('shipments.id'))
    
