import datetime
from project.database import Base, db

# from project.model.manufacture_product_junction import manufacture_product_junction
# from project.model.product import Product

class Manufacture(Base):
    __tablename__ = 'manufacture'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    review = db.Column(db.Text, nullable=True)
    details =  db.Column(db.PickleType, nullable=True)
    products = db.relationship('Product', secondary='manufacture_product_junction', back_populates='manufactures')
