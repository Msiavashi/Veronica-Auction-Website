
from project.database import Base, db
from project.logger import Logger
import datetime

class Payment(Base):
    __tablename__ = 'payment'
    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    payment_id = db.Column(db.String(length=25))
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))
