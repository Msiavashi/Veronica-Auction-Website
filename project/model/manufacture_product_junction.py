from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

manufacture_product_junction = Table('manufacture_product_junction', Base.metadata,
    Column('manufacturer_id', ForeignKey('manufacture.id')),
    Column('product_id', ForeignKey('product.id'))
)