from project.database import db, Base
from user import User
from payment import Payment
from payment_plan import payment_plans
from user_plan import user_plans


class Plan(Base):
    __tablename__ = 'plans'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    total_offers = db.Column(db.Integer, default=0)
    users = db.relationship('User', secondary = user_plans, back_populates='plans')
    payments = db.relationship('Payment', secondary = payment_plans, back_populates='plans')
