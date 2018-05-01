from project.database import db, Base
from manufacture_product import manufacture_products

class Manufacture(Base):
    __tablename__ = 'manufactures'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    country = db.Column(db.String(length=100), nullable=False)
    review = db.Column(db.Text, nullable=True)
    details =  db.Column(db.PickleType, nullable=True)
    products = db.relationship('Product', secondary=manufacture_products, back_populates='manufactures')
