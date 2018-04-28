import datetime
from project.database import Base, db, ma
from project.model.customer_plan_junction import customer_plan_junction
from project.model.customer import Customer 
# from project.model.auction import Auction

class Plan(Base):
    __tablename__ = 'plan'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    total_bids = db.Column(db.Integer, default=0)
    auctions = db.relationship('Auction')
    customers = db.relationship('Customer', secondary='customer_plan_junction', back_populates='plans')

class PlanSchema(ma.ModelSchema):
    class Meta:
        model = Plan 