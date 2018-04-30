from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
import datetime
from project.database import Base
from comment import Comment
from address import Address
from payment import Payment
from order import Order
from user_plan import user_plans
from user_gift import user_gifts
from user_role import user_roles
from user_auction import user_auctions
from user_product_view import user_product_views
from user_product_like import user_product_likes

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=255), nullable=False)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    work_place = Column(String(length=100))
    mobile = Column(String(length=15), nullable=False)
    email = Column(String(length=255))
    password = Column(String(length=100), nullable=False)

    #please check for dafault avatar address from config file
    avatar = Column(String(length=300))

    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now)

    #credit for each user
    credit = Column(DECIMAL(precision=20, scale=4), default=0)

    comments = relationship('Comment')
    address_id = Column(BigInteger, ForeignKey('addresses.id'))
    address = relationship('Address')
    payments = relationship('Payment')
    orders = relationship('Order')
    likes = relationship('Product', secondary=user_product_likes ,back_populates='products')
    views = relationship('Product', secondary=user_product_views ,back_populates='products')

    roles = relationship('Role',secondary=user_roles,back_populates='users')
    plans = relationship('Plan', secondary=user_plans, back_populates='users')
    gifts = relationship('Gift', secondary=user_gifts, back_populates='users')
    auctions = relationship('Auction', secondary=user_auctions,back_populates='users')
