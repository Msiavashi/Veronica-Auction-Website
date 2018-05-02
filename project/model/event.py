from project.database import db, Base
import datetime
from auction_event import auction_events
from product_event import product_events
from marshmallow import Schema, fields

class Event(Base):

    __tablename__ = 'events'
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4))
    auctions = db.relationship('Auction', secondary = auction_events, back_populates='events')
    products = db.relationship('Product', secondary = product_events, back_populates='events')

class EventSchema(Schema):
    id = fields.Int()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    discount = fields.Decimal()
    auctions = fields.Nested('AuctionSchema', many=True)
    products = fields.Nested('ProductSchema', many=True)
