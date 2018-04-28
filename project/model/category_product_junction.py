from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

category_product_junction = Table('category_product_junction', Base.metadata, 
    Column('product_id', ForeignKey('product.id')),
    Column('category_id', ForeignKey('category.id')))