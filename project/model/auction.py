# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime


class Auction(Base):
    __tablename__ = 'auctions'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    base_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_members = db.Column(db.BigInteger,default=40,nullable=False)
    ratio = db.Column(db.Integer,default=3,nullable=False)

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'),nullable=False)
    item = db.relationship('Item')

    participants = db.relationship('UserAuctionParticipation')

    offers = db.relationship('Offer')

    event_id = db.Column(db.BigInteger,db.ForeignKey('events.id'))
    event = db.relationship('Event')

    advertisement_id = db.Column(db.BigInteger,db.ForeignKey('advertisements.id'))
    advertisement = db.relationship('Advertisement')

    views = db.relationship('User', secondary = 'user_auction_views', back_populates='auction_views')
    likes = db.relationship('User', secondary = 'user_auction_likes', back_populates='auction_likes')

    plans = db.relationship('AuctionPlan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.name + " تاریخ شروع : " + str(self.start_date) + " تاریخ پایان : " + str(self.end_date)

class AuctionSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    base_price = fields.Str()
    max_price = fields.Str()
    max_members = fields.Str()
    ratio = fields.Int()

    item = fields.Nested('ItemSchema')
    participants = fields.Nested('UserSchema', many=True,exclude=('auctions',))
    offers = fields.Nested('OfferSchema', many=True,exclude=('auction',))
    likes = fields.Nested('LikeAuctionSchema', many=True,exclude=('auction',))
    views = fields.Nested('ViewAuctionSchema', many=True,exclude=('auction',))

    plans = fields.Nested('AuctionPlanSchema', many=True,exclude=('auction',))

    event = fields.Nested('EventSchema',exclude=('auction',))

    advertisement = fields.Nested('AdvertisementSchema',exclude=('auction',))
