
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

Insurance_Item_Junction = Table('insurance_item_junction', Base.metadata,
    Column('insurance_id', ForeignKey('insurance.id')),
    Column('item_id', ForeignKey('item.id'))
)
