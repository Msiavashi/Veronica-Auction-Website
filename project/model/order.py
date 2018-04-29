import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
#from project.model.offer import Offer
from shipment import Shipment

class Order(Base):

    __tablename__ = 'order'

    id = Column(BigInteger, primary_key=True)
    create_date = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    offers = relationship('Offer')
    shipments = relationship('Shipment')
