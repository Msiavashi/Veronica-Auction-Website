# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class AuctionPlan(Base):
    __tablename__ = 'auction_plans'

    id = db.Column(db.BigInteger,primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)
    max_offers = db.Column(db.Integer,nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)

    auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id'))
    plan = db.relationship('Plan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return self.plan.title + " " + self.auction.title
        except Exception as e:
            return " بدون حراجی "


class AuctionPlanSchema(Schema):
    id = fields.Int()
    price = fields.Int()
    max_offers = fields.Int()
    discount = fields.Str()
    auction = fields.Nested('AuctionSchema',exclude=('plans',))
    plan = fields.Nested('PlanSchema',exclude=('auctions',))
