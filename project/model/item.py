from project.database import db, Base
from offer import Offer
from insurance_item import insurance_items
from payment_item import payment_items
from order_item import order_items
from inventory_item import inventory_items
from marshmallow import Schema, fields

class Item(Base):
    __tablename__ = 'items'
    id = db.Column(db.BigInteger, primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4))
    auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')
    inventory_id = db.Column(db.BigInteger, db.ForeignKey('inventories.id'))
    inventories = db.relationship('Inventory', secondary = inventory_items , back_populates='items')
    offers = db.relationship('Offer',back_populates = 'item')
    insurances = db.relationship('Insurance', secondary = insurance_items, back_populates='items')
    payments = db.relationship('Payment', secondary = payment_items,back_populates='items')
    orders = db.relationship('Order', secondary = order_items, back_populates='items')

class ItemSchema(Schema):
    id = fields.Int()
    price = fields.Decimal()
    discount = fields.Decimal()
    auction = fields.Nested('AuctionSchema')
    product = fields.Nested('ProductSchema')
    inventories = fields.Nested('InventorySchema', many=True)
    offers = fields.Nested('OfferSchema',many=True)
    insurances = fields.Nested('InsuranceSchema',many=True)
    payments = fields.Nested('PaymentSchema',many=True)
    orders = fields.Nested('OrderSchema',many=True)
