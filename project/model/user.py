from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
import datetime
from project.database import Base
from role import Role
from comment import Comment
from address import Address
from payment import Payment
from order import Order
from user_plan_junction import user_plan_junction
from user_gift_junction import user_gift_junction
from project import ma

class User(Base):
    __tablename__ = 'user'
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

    #each user may have an advisor_code that can be used for one time and has 20$ credit for them
    expired_advisor = Column(Boolean,default=False)
    advisor_code = Column(String(length=255))

    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now)

    #credit for each user
    credit = Column(DECIMAL(precision=20, scale=4), default=0)

    roles = relationship('Role')
    comments = relationship('Comment')
    address_id = Column(BigInteger, ForeignKey('address.id'))
    payments = relationship('Payment')
    orders = relationship('Order')
    plans = relationship('Plan', secondary=user_plan_junction, back_populates='users')
    gifts = relationship('Gift',secondary=user_gift_junction, back_populates='users')
    #Auction

