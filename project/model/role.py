from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
from sqlalchemy.types import BigInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
import datetime
from project.database import Base
# from project.model.customer import Customer


class Role(Base):
    __tablename__ = 'role'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(512))
    customer_id = Column(BigInteger, ForeignKey('customer.id'))

