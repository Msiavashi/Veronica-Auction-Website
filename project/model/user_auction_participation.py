from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class UserAuctionParticipation(Base):
    __tablename__ = 'user_auction_participations'

    id = db.Column(db.BigInteger,primary_key=True)
    
    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    plan_id = db.Column(db.BigInteger,db.ForeignKey('plans.id'))
    plan = db.relationship('Plan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
