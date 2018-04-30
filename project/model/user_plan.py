from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

user_plans = Table('user_plans', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('plan_id', ForeignKey('plans.id')),
    Column('used',Boolean,default=False)
)
