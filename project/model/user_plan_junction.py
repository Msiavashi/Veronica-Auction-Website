from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

user_plan_junction = Table('user_plan_junction', Base.metadata,
    Column('user_id', ForeignKey('user.id')),
    Column('plan_id', ForeignKey('plan.id'))
)
