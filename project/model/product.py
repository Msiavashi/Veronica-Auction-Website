from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Product(Base):

    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    desciption = db.Column(db.Text,nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)

    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products')

    items = db.relationship('Item')

    comments = db.relationship("Comment")

    manufacture_id = db.Column(db.BigInteger,db.ForeignKey('manufactures.id'))
    manufacture = db.relationship('Manufacture')

    advertisement_id = db.Column(db.BigInteger,db.ForeignKey('advertisements.id'))
    advertisement = db.relationship('Advertisement')

    inventories = db.relationship('Inventory', secondary='inventory_products' ,back_populates='products')

    garanties = db.relationship('Garanty', secondary='garanty_products' ,back_populates='products')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title


class ProductSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    desciption = fields.Str()
    quantity = fields.Int()
    details = fields.Str()
    category = fields.Nested('CategorySchema',exclude=('products',))
    items = fields.Nested('ItemSchema',many=True,exclude=('product',))
    comments = fields.Nested('CommentSchema',many=True,exclude=('product',))
    inventories = fields.Nested('InventorySchema',many=True,exclude=('products',))
    events = fields.Nested('EventSchema',many=True,exclude=('products',))
    manufacture = fields.Nested('ManufactureSchema',exclude=('products',))
    garanties = fields.Nested('GarantySchema',many=True,exclude=('products',))
    advertisement = fields.Nested('AdvertisementSchema',exclude=('auction',))
