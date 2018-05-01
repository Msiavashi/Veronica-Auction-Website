from project.database import db, Base
import datetime
from shipment import Shipment


class Order(Base):

    __tablename__ = 'orders'

    id = db.Column(db.BigInteger, primary_key=True)
    create_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    items = db.relationship('Item',back_populates='orders')
    shipments = db.relationship('Shipment',back_populates='orders')
