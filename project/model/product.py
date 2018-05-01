from project.database import db, Base
from manufacture_product import manufacture_products
from manufacture import Manufacture
from category import Category


class Product(Base):

    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    details =  db.Column(db.PickleType, nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category',back_populates='products')
    items = db.relationship('Item')
    comments = db.relationship("Comment")
    events = db.relationship("ProductEvent")
    manufactures = db.relationship('Manufacture', secondary=manufacture_products, back_populates='products')
