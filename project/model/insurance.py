import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from insurance_item_junction import Insurance_Item_Junction
# from project.model.item import Item

class Insurance(Base):
    __tablename__ = "insurance"
    id = Column(BigInteger, primary_key=True)
    company_name = Column(String(length=100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    items = relationship('Item', secondary=Insurance_Item_Junction, back_populates='insurances')
    # insurance_serial = Column(String(100))
