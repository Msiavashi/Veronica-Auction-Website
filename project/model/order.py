import datetime
# from flask_marshmallow import fields
from project.database import Base, db
# from project.model.offer import Offer 
from project.model.shipment import Shipment 

class Order(Base):

    __tablename__ = 'order'
 
    id = db.Column(db.BigInteger, primary_key=True)
    create_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    modify_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    custormer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))
    offers = db.relationship('Offer')
    shipments = db.relationship('Shipment')

