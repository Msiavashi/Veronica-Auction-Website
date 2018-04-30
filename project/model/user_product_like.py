from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

user_product_likes = Table('user_product_likes', Base.metadata,
    Column('product_id', ForeignKey('products.id')),
    Column('user_id', ForeignKey('users.id'))
)
