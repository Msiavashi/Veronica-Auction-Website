
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
import datetime
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.orm import relationship
from project.database import Base
from product import Product

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(length=255), nullable=False)
    message = Column(String(length=2048), nullable=False)
    likes = Column(Integer, default=0)
    date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User')
    product_id = Column(BigInteger, ForeignKey('products.id'))
    product = relationship('Product')
