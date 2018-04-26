import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL, PickleType
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from category_product_junction import category_product_junction
from category import Category 
from comment import Comment
# from project.model.item import Item
from manufacture_product_junction import manufacture_product_junction
from manufacture import Manufacturer


class Product(Base):

    __tablename__ = 'product'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=25))
    total_available = Column(Integer)
    review = Column(Text)
    stars = Column(Integer)
    details =  Column(PickleType)
    items = relationship('Item')
    categories = relationship('Category', secondary=category_product_junction, back_populates='products')
    comments = relationship("Comment")

    manufactures = relationship('Manufacture', secondary=manufacture_product_junction, back_populates='products')