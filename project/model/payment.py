from project.database import db, Base
import datetime
from .payment_item import payment_items
from .payment_plan import payment_plans
from marshmallow import Schema , fields

class Payment(Base):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    guid = db.Column(db.String(length=50))
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    method = db.Column(db.PickleType)
    status = db.Column(db.Boolean)
    details = db.Column(db.PickleType)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    plans = db.relationship('Plan',secondary=payment_plans,back_populates='payments')
    items = db.relationship('Item',secondary=payment_items,back_populates='payments')
    def __str__(self):
        return self.guid + "status :" + self.status

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Decimal()
    guid = fields.Str()
    date = fields.DateTime()
    method = fields.Raw()
    details = fields.Raw()
    user = fields.Nested('User')
    plans = fields.Nested('PlanSchema', many=True)
    items = fields.Nested('ItemSchema', many=True)
