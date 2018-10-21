from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Offer(Base):
    __tablename__ = 'offers'

    id = db.Column(db.BigInteger, primary_key=True)

    total_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    current_bids = db.Column(db.Integer,nullable=False)
    win = db.Column(db.Boolean,default=False)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

class OfferSchema(Schema):
    id = fields.Int()
    total_price = fields.Str()
    status = fields.Int()
    win = fields.Boolean()
    created_at = fields.DateTime()
    winner = fields.Str()
    auction = fields.Nested('AuctionSchema',exclude=('offers',))
