import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from item import Item
from project.database import Base
from item import Item
from plan import Plan 

class Auction(Base):
    __tablename__ = 'auction'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    minimum_price_increment = Column(DECIMAL(precision=20, scale=4), nullable=False)
    items = relationship('Item')
    plan_id = Column(BigInteger, ForeignKey('plan.id'))