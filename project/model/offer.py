from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Offer(Base):
    __tablename__ = 'offers'

    id = db.Column(db.BigInteger, primary_key=True)
    offer_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    status = db.Column(db.Integer,default=0,nullable=False)
    win = db.Column(db.Boolean,default=False)

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    plan_id = db.Column(db.BigInteger,db.ForeignKey('plans.id'))
    plan = db.relationship('Plan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

class OfferSchema(Schema):
    id = fields.Int()
    offer_price = fields.Str()
    status = fields.Int()
    win = fields.Boolean()
    created_at = fields.DateTime()

    user = fields.Nested('UserSchema',exclude=('offers',))
    auction = fields.Nested('AuctionSchema',exclude=('offers',))
    plan = fields.Nested('PlanSchema',exclude=('offers',))
