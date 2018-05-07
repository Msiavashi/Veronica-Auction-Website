from project.database import db, Base
from .offer import Offer
from .insurance_item import insurance_items
from .payment_item import payment_items
from .order_item import order_items
from .inventory_item import inventory_items
from marshmallow import Schema, fields

class Item(Base):
    __tablename__ = 'items'
    id = db.Column(db.BigInteger, primary_key=True)
    model = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text())
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    discount = db.Column(db.Integer())
    # auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    # auction = db.relationship('Auction')
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')
    inventory_id = db.Column(db.BigInteger, db.ForeignKey('inventories.id'))
    inventories = db.relationship('Inventory', secondary = inventory_items , back_populates='items')
    offers = db.relationship('Offer',back_populates = 'item')
    insurances = db.relationship('Insurance', secondary = insurance_items, back_populates='items')
    payments = db.relationship('Payment', secondary = payment_items,back_populates='items')
    orders = db.relationship('Order', secondary = order_items, back_populates='items')
    def __str__(self):
        return self.product.name + " " + self.model

class ItemSchema(Schema):
    id = fields.Int()
    price = fields.Str()
    discount = fields.Int()
    auction = fields.Nested('AuctionSchema',exclude=('item',))
    product = fields.Nested('ProductSchema',exclude=('items',))
    inventories = fields.Nested('InventorySchema', many=True,exclude=('items',))
    offers = fields.Nested('OfferSchema',many=True,exclude=('items',))
    insurances = fields.Nested('InsuranceSchema',many=True,exclude=('items',))
    payments = fields.Nested('PaymentSchema',many=True,exclude=('items',))
    orders = fields.Nested('OrderSchema',many=True,exclude=('items',))
