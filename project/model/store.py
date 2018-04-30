import datetime
from project.database import Base, db
# from project.model.address import Address
# from project.model.item import Item 


class Store(Base):
    __tablename__ = 'store'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=True)
    desciption = db.Column(db.String(length=255), nullable=True)
    items = db.relationship('Item') 
    address_id = db.Column(db.BigInteger, db.ForeignKey('address.id'))