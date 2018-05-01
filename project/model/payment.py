from project.database import db, Base
import datetime
from payment_item import payment_items
from payment_plan import payment_plans

class Payment(Base):
    __tablename__ = 'payments'
    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    guid = db.Column(db.String(length=50))
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    method = db.Column(db.PickleType)
    details = db.Column(db.PickleType)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    plans = db.relationship('Plan',secondary=payment_plans,back_populates='payments')
    items = db.relationship('Item',secondary=payment_items,back_populates='payments')
