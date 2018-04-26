import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from manufacture_product_junction import manufacture_product_junction
# from project.model.product import Product

class Manufacturer(Base):
    __tablename__ = 'manufacture'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=25))
    review = Column(Text)
    details =  Column(PickleType)
    products = relationship('Product', secondary=manufacture_product_junction, back_populates='manufactures')
