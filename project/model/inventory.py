from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Inventory(Base):
    __tablename__ = 'inventories'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=255), nullable=False)

    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address')

    products = db.relationship('Product', secondary = 'inventory_products' , back_populates = 'inventories')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.name

class InventorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    products = fields.Nested('ProductSchema',many=True,exclude=('inventories',))
    address = fields.Nested('AddressSchema')
