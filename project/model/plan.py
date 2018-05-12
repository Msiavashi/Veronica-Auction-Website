from project.database import db, Base
from marshmallow import Schema , fields

class Plan(Base):
    __tablename__ = 'plans'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    total_offers = db.Column(db.Integer, default=0)
    users = db.relationship('User', secondary = 'user_plans', back_populates='plans')
    payments = db.relationship('Payment', secondary = 'payment_plans', back_populates='plans')
    def __str__(self):
        return self.name
class PlanSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Str()
    total_offers = fields.Int()
    users = fields.Nested('UserSchema', many=True,exclude=('plans',))
    payments = fields.Nested('PaymentSchema',many=True,exclude=('plans',))
