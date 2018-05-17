from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class UserPlan(Base):
    __tablename__ = 'user_plans'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    auction_plan_id = db.Column(db.BigInteger,db.ForeignKey('auction_plans.id'))
    auction_plan = db.relationship('AuctionPlan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

class UserPlanSchema(Schema):
    user = fields.Nested('UserSchema',exclude=('user_plans',))
