import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from user_gift import user_gifts

class Gift(Base):
    __tablename__ = 'gifts'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    amount = Column(DECIMAL(precision=20, scale=4), nullable=True)
    users = relationship('User', secondary=user_gifts, back_populates='gifts')
