from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from project.database import Base

user_auctions = Table('user_auctions', Base.metadata,
    Column('auction_id', ForeignKey('auctions.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('date',TIMESTAMP,default=datetime.datetime.now)
)
