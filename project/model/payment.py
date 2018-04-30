from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL,PickleType
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base
from project.logger import Logger
import datetime
from payment_item import payment_items
from payment_plan import payment_plans

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(BigInteger, primary_key=True)
    amount = Column(DECIMAL(precision=20, scale=4), nullable=False)
    guid = Column(String(length=50))
    date = Column(TIMESTAMP, default=datetime.datetime.now)
    method = Column(PickleType)
    details = Column(PickleType)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User')
    plans = relationship('Plan',secondary=payment_plans,back_populates='payments')
    items = relationship('Item',secondary=payment_items,back_populates='payments')
