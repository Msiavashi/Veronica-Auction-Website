from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Plan(Base):
    __tablename__ = 'plans'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    auctions = db.relationship('AuctionPlan')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title

class PlanSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    auctions = fields.Nested('AuctionPlanSchema',many=True,exclude=('plan',))
