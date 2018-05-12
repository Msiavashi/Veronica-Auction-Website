from project.database import db, Base
import datetime
from marshmallow import Schema, fields

class Event(Base):

    __tablename__ = 'events'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255))
    description = db.Column(db.Text)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    discount = db.Column(db.Integer,default=0)
    active = db.Column(db.Boolean,default=False)
    auctions = db.relationship('Auction', secondary = 'auction_events', back_populates='events')
    products = db.relationship('Product', secondary = 'product_events', back_populates='events')
    def __str__(self):
        return self.title

class EventSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    discount = fields.Str()
    active = fields.Boolean()
    auctions = fields.Nested('AuctionSchema', many=True,exclude=('events',))
    products = fields.Nested('ProductSchema', many=True,exclude=('events',))
