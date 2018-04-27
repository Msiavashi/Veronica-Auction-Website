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
from customer_plan_junction import customer_plan_junction
# from project.model.plan import Plan

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    username = Column(String(length=30), nullable=False)
    password = Column(String(length=30), nullable=False)
    register_date = Column(TIMESTAMP, default=datetime.datetime.now)
    phone_number = Column(String(length=25), nullable=False)
    email = Column(String(length=100))
    credit = Column(DECIMAL(precision=20, scale=4), default=0)
    gift_credit = Column(DECIMAL(precision=20, scale=4), default=0)
    organization_or_person = Column(String(length=20), nullable=False)
    roles = relationship('Role')
    comments = relationship('Comment')
    address_id = Column(BigInteger, ForeignKey('address.id'))
    payments = relationship('Payment')
    orders = relationship('Order')

    plans = relationship('Plan', secondary=customer_plan_junction, back_populates='customers')

    