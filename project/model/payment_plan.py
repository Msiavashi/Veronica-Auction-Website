from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

payment_plans = Table('payment_plans', Base.metadata,
    Column('payment_id', ForeignKey('payments.id')),
    Column('plan_id', ForeignKey('plans.id'))
)
