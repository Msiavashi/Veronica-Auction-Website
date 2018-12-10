# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
import datetime

class AuctionNotificationType:
    REGULAR = 1
    FINISHED = 2
    REMINDER = 3

class AuctionNotification(Base):
    __tablename__ = 'auction_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(length=1024))
    type = db.Column(db.Integer,nullable=False)
    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'),nullable=False)
    auction = db.relationship('Auction')
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
