import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from user import User

class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True)
    offer_price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    date = Column(TIMESTAMP, default=datetime.datetime.now)

    user_id = Column(BigInteger,ForeignKey('users.id'))
    user = relationship('User')
    item_id = Column(BigInteger, ForeignKey('items.id'))
    item = relationship('Item')
    win = Column(Boolean,default=False)
