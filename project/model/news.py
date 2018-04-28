import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

class News(Base):
    __tablename__ = 'news'
    id = Column(BigInteger, primary_key=True)
    title = Column(String(length=100),nullable=False)
    description = Column(String(length=1000))
    images = Column(PickleType)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
