from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

user_gifts = Table('user_gifts', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('gift_id', ForeignKey('gifts.id')),
    Column('used',Boolean,default=False)
)
