from project.database import db, Base
from .address import Address
from marshmallow import Schema, fields
from .inventory_item import inventory_items

class Inventory(Base):
    __tablename__ = 'inventories'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    desciption = db.Column(db.String(length=255), nullable=True)
    items = db.relationship('Item', secondary = inventory_items , back_populates = 'inventories')
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address')
    def __str__(self):
        return self.name

class InventorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    desciption = fields.Str()
    items = fields.Nested('ItemSchema',many=True)
    address = fields.Nested('AddressSchema')
