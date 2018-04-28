
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
# from project.model.insurance import Insurance
# from project.model.item import Item 

insurance_item_junction = Table('insurance_item_junction', Base.metadata,
    Column('insurance_id', ForeignKey('insurance.id')),
    Column('item_id', ForeignKey('item.id'))
)