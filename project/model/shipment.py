from project.database import db, Base
import datetime
from marshmallow import Schema, fields

class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)
    company = db.Column(db.String(length=100), nullable=False)
    method = db.Column(db.String(length=100), nullable=False)
    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    vehicle = db.Column(db.String(length=35), nullable=True)
    status = db.Column(db.Boolean)
    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'))
    insurance = db.relationship('Insurance')
    order = db.relationship('Order',back_populates = 'shipment')
    def __str__(self):
        return str(self)

class ShipmentSchema(Schema):
    id = fields.Int()
    company = fields.Str()
    method = fields.Str()
    send_date = fields.DateTime()
    recieve_date = fields.DateTime()
    price = fields.Str()
    vehicle = fields.Str()
    status = fields.Boolean()
    insurance = fields.Nested('InsuranceSchema',exclude=('shipment',))
    order = fields.Nested('OrderSchema',exclude=('shipment',))
