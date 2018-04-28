from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base 
import json
from product import Product
from offer import Offer 
from store import Store 
# from project.model.auction import Auction
from insurance_item_junction import insurance_item_junction
from insurance import Insurance

class Item(Base):
    __tablename__ = 'item'
    id = Column(BigInteger, primary_key=True)
    price = Column(DECIMAL(precision=20, scale=4), nullable=True)
    off = Column(DECIMAL(precision=20, scale=4))
    made_in = Column(String(length=25))
    auction_id = Column(BigInteger, ForeignKey('auction.id'))
    product_id = Column(BigInteger, ForeignKey('product.id'))
    offers = relationship('Offer')
    store_id = Column(BigInteger, ForeignKey('store.id'))
    insurances = relationship('Insurance', secondary=insurance_item_junction, back_populates='items')
