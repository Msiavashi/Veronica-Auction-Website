from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base , db

import json
# from project.model.product import Product
# from project.model.offer import Offer 
# from project.model.store import Store 
# from project.model.auction import Auction
# from project.model.insurance_item_junction import insurance_item_junction
# from project.model.insurance import Insurance

class Item(Base):
    __tablename__ = 'item'
    id = db.Column(db.BigInteger, primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    off = db.Column(db.DECIMAL(precision=20, scale=4), default=0)
    made_in = db.Column(db.String(length=25))
    auction_id = db.Column(db.BigInteger, db.ForeignKey('auction.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'))
    offers = db.relationship('Offer')
    store_id = db.Column(db.BigInteger, db.ForeignKey('store.id'))
    insurances = db.relationship('Insurance', secondary='insurance_item_junction', back_populates='items')