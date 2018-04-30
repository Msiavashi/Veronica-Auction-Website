import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
from item import Item
from user_auction import user_auctions

class Auction(Base):
    __tablename__ = 'auctions'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = Column(TIMESTAMP, default=datetime.datetime.now, nullable=False)
    register_price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    minimum_price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    maximum_price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    max_members = Column(BigInteger,default=40)

    item_id = Column(BigInteger, ForeignKey('items.id'))
    item = relationship('Item')
    users = relationship('User',secondary=user_auctions,back_populates='auctions')
    events = relationship('AuctionEvent')
