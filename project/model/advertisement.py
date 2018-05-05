from project.database import db, Base
import datetime
from .auction_event import auction_events
from .product_event import product_events
from marshmallow import Schema, fields

class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100),nullable=False)
    description = db.Column(db.String(length=100),nullable=False)
    images = db.Column(db.PickleType,nullable=False)
    link = db.Column(db.String(length=255),nullable=False)
    link_title = db.Column(db.String(length=100),nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now,)
    auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction', back_populates = 'advertisement')
    def __str__(self):
        return self.title + " " + auction

class AdvertisementSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    images = fields.Raw()
    link =fields.Url()
    link_title =fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    auction = fields.Nested('AuctionSchema')
