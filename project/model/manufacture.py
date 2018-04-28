import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from manufacture_product_junction import Manufacture_Product_Junction
# from project.model.product import Product

class Manufacture(Base):
    __tablename__ = 'manufacture'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=25), nullable=False)
    review = Column(Text, nullable=True)
    details =  Column(PickleType, nullable=True)
    products = relationship('Product', secondary=Manufacture_Product_Junction, back_populates='manufactures')
