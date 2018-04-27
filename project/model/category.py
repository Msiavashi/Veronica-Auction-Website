import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
 
class Category(Base):
    __tablename__ = 'category'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=30))
    categories = relationship('Category', remote_side=[id])
    category_id = Column(BigInteger, ForeignKey('category.id'))

    products = relationship('Product')
    

    