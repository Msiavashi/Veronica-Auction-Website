# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
import datetime

class UserAuctionNotification(Base):
    __tablename__ = 'user_auction_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    auction_notification_id = db.Column(db.BigInteger,db.ForeignKey('auction_notifications.id'))
    auction_notification = db.relationship('AuctionNotification')

    delivered = db.Column(db.Boolean,default=True)
    seen = db.Column(db.Boolean,default=False)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


    def __str__(self):
        return str(self.notification) +" - "+ str(self.user)
