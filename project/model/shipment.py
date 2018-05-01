from project.database import db, Base
import datetime
from insurance import Insurance



class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)
    transport_company = db.Column(db.String(length=100), nullable=False)
    transport_method = db.Column(db.String(length=100), nullable=False)
    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    transport_vehicle = db.Column(db.String(length=35), nullable=True)
    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'))
    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'))
    
