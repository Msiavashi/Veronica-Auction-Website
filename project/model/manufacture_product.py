from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

manufacture_products = Table('manufacture_products', Base.metadata,
    Column('manufacture_id', ForeignKey('manufactures.id')),
    Column('product_id', ForeignKey('products.id'))
)
