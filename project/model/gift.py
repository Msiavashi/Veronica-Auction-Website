import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from user_gift_junction import user_gift_junction
from user import User
# from project.model.auction import Auction

class Gift(Base):
    __tablename__ = 'gift'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    amount = Column(DECIMAL(precision=20, scale=4), nullable=True)
    users = relationship('User', secondary=user_gift_junction, back_populates='gifts')
