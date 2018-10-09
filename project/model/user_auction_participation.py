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

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
     updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


class UAPSchema(Schema):
    auction = fields.Nested('AuctionSchema',exclude=('participants',))
    user = fields.Nested('UserSchema',exclude=('auctions',))
