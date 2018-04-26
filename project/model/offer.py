import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from order import Order 
# from project.model.item import Item 

class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True)
    offer_price = Column(DECIMAL(precision=20, scale=4))
    date = Column(TIMESTAMP, default=datetime.datetime.now)
    order_id = Column(BigInteger, ForeignKey('order.id'))
    item_id = Column(BigInteger, ForeignKey('item.id'))
