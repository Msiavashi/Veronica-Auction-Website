from project.database import db, Base
from .insurance_item import insurance_items
from marshmallow import Schema, fields


class Insurance(Base):
    __tablename__ = "insurances"
    id = db.Column(db.BigInteger, primary_key=True)
    company_name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item', secondary=insurance_items, back_populates='insurances')
    def __str__(self):
        return self.company_name

class InsuranceSchema(Schema):
    id = fields.Int()
    company_name = fields.Str()
    description = fields.Str()
    price = fields.Decimal()
    items = fields.Nested("ItemSchema",many=True)
