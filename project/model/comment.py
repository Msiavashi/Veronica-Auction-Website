
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
import datetime
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base
# from project.model.product import Product


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(length=255))
    message = Column(String(length=2048))
    stars = Column(Integer)
    customer_id = Column(BigInteger, ForeignKey('customer.id'))
    product_id = Column(BigInteger, ForeignKey('product.id'))
