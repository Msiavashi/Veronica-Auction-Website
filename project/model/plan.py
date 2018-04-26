import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from customer_plan_junction import customer_plan_junction
from customer import Customer 
# from project.model.auction import Auction

class Plan(Base):
    __tablename__ = 'plan'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100))
    price = Column(DECIMAL(precision=20, scale=4))
    total_bids = Column(Integer)
    auctions = relationship('Auction')
    customers = relationship('Plan', secondary=customer_plan_junction, back_populates='plans')
