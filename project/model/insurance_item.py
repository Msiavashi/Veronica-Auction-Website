
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

insurance_items = Table('insurance_items', Base.metadata,
    Column('insurance_id', ForeignKey('insurances.id')),
    Column('item_id', ForeignKey('items.id'))
)
