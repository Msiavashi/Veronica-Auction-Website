import datetime
from project.database import Base, db
# from project.model.order import Order 
# from project.model.insurance import Insurance



class Shipment(Base):
    __tablename__ = 'shipment'
    id = db.Column(db.BigInteger, primary_key=True)
    transport_company = db.Column(db.String(length=100), nullable=False)    
    transport_method = db.Column(db.String(length=100), nullable=False)
    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    transport_vehicle = db.Column(db.String(length=35), nullable=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'))
    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurance.id'))

