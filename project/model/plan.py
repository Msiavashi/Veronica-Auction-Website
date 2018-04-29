import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from user_plan_junction import user_plan_junction
from user import User
# from project.model.auction import Auction

class Plan(Base):
    __tablename__ = 'plan'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    price = Column(DECIMAL(precision=20, scale=4), nullable=True)
    total_bids = Column(Integer, default=0)
    auctions = relationship('Auction')
    users = relationship('User', secondary=user_plan_junction, back_populates='plans')
