from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base
from project.logger import Logger
import datetime

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(BigInteger, primary_key=True)
    amount = Column(DECIMAL(precision=20, scale=4), nullable=False)
    payment_id = Column(String(length=25))
    date = Column(TIMESTAMP, default=datetime.datetime.now)
    user_id = Column(BigInteger, ForeignKey('user.id'))
