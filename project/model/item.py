from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
import json
from offer import Offer
from insurance_item import insurance_items
from payment_item import payment_items

class Item(Base):
    __tablename__ = 'items'
    id = Column(BigInteger, primary_key=True)
    price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    discount = Column(DECIMAL(precision=20, scale=4))

    auction_id = Column(BigInteger, ForeignKey('auctions.id'))
    auction = relationship('Auction')
    product_id = Column(BigInteger, ForeignKey('products.id'))
    product = relationship('Product')
    inventory_id = Column(BigInteger, ForeignKey('inventories.id'))
    inventory = relationship('Inventory')
    offers = relationship('Offer',back_populates='items')
    insurances = relationship('Insurance', secondary=insurance_items, back_populates='items')
    payments = relationship('Payment', secondary=payment_items,back_populates='items')
