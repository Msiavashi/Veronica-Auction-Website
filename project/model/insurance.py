from project.database import db, Base
from marshmallow import Schema, fields
import datetime


class Insurance(Base):
    __tablename__ = "insurances"
    id = db.Column(db.BigInteger, primary_key=True)
    company = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text,nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    shipments = db.relationship('Shipment')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    def __str__(self):
        return self.company_name

class InsuranceSchema(Schema):
    id = fields.Int()
    company = fields.Str()
    description = fields.Str()
    price = fields.Str()
    shipments = fields.Nested("ShipmentSchema",many=True,exclude=('insurances',))
