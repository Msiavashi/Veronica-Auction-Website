from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from project.database import Base

user_product_views = Table('user_product_views', Base.metadata,
    Column('product_id', ForeignKey('products.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('ip_address',String(length=64)),
    Column('date',TIMESTAMP, default=datetime.datetime.now)
)
