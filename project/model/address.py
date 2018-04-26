from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
import datetime
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base

class Address(Base):
    __tablename__ = 'address'
    id = Column(BigInteger, primary_key=True)
    country = Column(String(length=25))
    city = Column(String(length=30))
    phone_number = Column(String(length=25))
    address = Column(String(length=255))
    postal_code = Column(String(length=30))
