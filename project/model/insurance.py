import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from insurance_item import insurance_items

class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(BigInteger, primary_key=True)
    company_name = Column(String(length=100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    items = relationship('Item', secondary=insurance_items, back_populates='insurances')
