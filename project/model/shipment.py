import datetime
from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, DECIMAL
from sqlalchemy.types import BigInteger, TIMESTAMP, Time, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base
# from project.model.order import Order
from insurance import Insurance



class Shipment(Base):
    __tablename__ = 'shipments'
    id = Column(BigInteger, primary_key=True)
    transport_company = Column(String(length=100), nullable=False)
    transport_method = Column(String(length=100), nullable=False)
    send_date = Column(TIMESTAMP, default=datetime.datetime.now)
    recieve_date = Column(TIMESTAMP, default=datetime.datetime.now)
    price = Column(DECIMAL(precision=20, scale=4), nullable=False)
    transport_vehicle = Column(String(length=35), nullable=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'))
    insurance_id = Column(BigInteger, ForeignKey('insurances.id'))
