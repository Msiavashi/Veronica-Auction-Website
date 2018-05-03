from project.database import db, Base
import datetime
from item import Item
from advertisement import Advertisement
from event import Event
from user_auction import user_auctions
from auction_event import auction_events
from user_auction_view import user_auction_views
from user_auction_like import user_auction_likes
from marshmallow import Schema, fields

class Auction(Base):
    __tablename__ = 'auctions'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    register_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    minimum_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    maximum_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_members = db.Column(db.BigInteger,default=40)
    item = db.relationship('Item')
    users = db.relationship('User',secondary = user_auctions,back_populates='auctions')
    events = db.relationship('Event', secondary = auction_events, back_populates='auctions')
    advertisement = db.relationship('Advertisement' , back_populates ='auction')
    auction_views = db.relationship('User', secondary = user_auction_views, back_populates='auction_views')
    auction_likes = db.relationship('User', secondary = user_auction_likes, back_populates='auction_likes')

class AuctionSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    register_price = fields.Decimal()
    minimum_price = fields.Decimal()
    maximum_price = fields.Decimal()
    max_members = fields.Int()
    item = fields.Nested('ItemSchema', many=True)
    users = fields.Nested('UserSchema', many=True)
    events = fields.Nested('EventSchema', many=True)
    advertisement = fields.Nested('AdvertisementSchema')
