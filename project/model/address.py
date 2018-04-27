from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
import datetime
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base

class Address(Base):
    __tablename__ = 'address'
    id = Column(BigInteger, primary_key=True)
    country = Column(String(length=25), nullable=False)
    city = Column(String(length=30), nullable=False)
    phone_number = Column(String(length=25), nullable=False)
    address = Column(String(length=255), nullable=False)
    postal_code = Column(String(length=30), nullable=False)
