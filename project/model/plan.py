import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from user import User
from payment import Payment
from payment_plan import payment_plans
from user_plan import user_plans


class Plan(Base):
    __tablename__ = 'plans'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    price = Column(DECIMAL(precision=20, scale=4), nullable=True)
    total_offers = Column(Integer, default=0)
    users = relationship('User', secondary = user_plans, back_populates='plans')
    payments = relationship('Payment', secondary = payment_plans, back_populates='plans')
