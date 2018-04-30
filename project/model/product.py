import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL, PickleType
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from manufacture_product import manufacture_products
from manufacture import Manufacture
from category import Category


class Product(Base):

    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=25), nullable=False)
    quantity = Column(Integer, nullable=False)
    review = Column(Text)
    likes = Column(Integer, default=0)
    details =  Column(PickleType, nullable=True)
    category_id = Column(BigInteger, ForeignKey('categories.id'))
    category = relationship('Category',back_populates='products')
    items = relationship('Item')
    comments = relationship("Comment")
    events = relationship("ProductEvent")
    manufactures = relationship('Manufacture', secondary=manufacture_products, back_populates='products')
    
