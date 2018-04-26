import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from address import Address
# from project.model.item import Item 


class Store(Base):
    __tablename__ = 'store'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=25))
    desciption = Column(String(length=255))
    items = relationship('Item') 
    address_id = Column(BigInteger, ForeignKey('address.id'))