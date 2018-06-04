from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class AuctionPlan(Base):
    __tablename__ = 'auction_plans'

    id = db.Column(db.BigInteger,primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)
    max_offers = db.Column(db.Integer,nullable=False)

    auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id'))
    plan = db.relationship('Plan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.plan.title + " " + self.auction.title

class AuctionPlanSchema(Schema):
    id = fields.Int()
    price = fields.Int()
    max_offers = fields.Int()
    auction = fields.Nested('AuctionSchema',exclude=('plans',))
    plan = fields.Nested('PlanSchema',exclude=('auctions',))
