import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from address import Address

class Inventory(Base):
    __tablename__ = 'inventories'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    desciption = Column(String(length=255), nullable=True)
    items = relationship('Item')
    address_id = Column(BigInteger, ForeignKey('addresses.id'))
    address = relationship('Address')
