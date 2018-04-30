import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL, PickleType
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base


class ProductEvent(Base):

    __tablename__ = 'product_events'
    id = Column(BigInteger, primary_key=True)
    start_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    products = relationship('Product')
    discount = Column(DECIMAL(precision=20, scale=4))
