from project.database import db, Base
from offer import Offer
from insurance_item import insurance_items
from payment_item import payment_items

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
    inventory = db.relationship('Inventory')
    offers = db.relationship('Offer',back_populates='items')
    insurances = db.relationship('Insurance', secondary=insurance_items, back_populates='items')
    payments = db.relationship('Payment', secondary=payment_items,back_populates='items')
