from project.database import db, Base
from address import Address

class Inventory(Base):
    __tablename__ = 'inventories'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    desciption = db.Column(db.String(length=255), nullable=True)
    items = db.relationship('Item')
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address')
