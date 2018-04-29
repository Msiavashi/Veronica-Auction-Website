import datetime
from project.database import db
from project.database import Base

class Address(Base):
    __tablename__ = 'address'
    id = db.Column(db.BigInteger, primary_key=True)
    country = db.Column(db.String(length=25), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    phone_number = db.Column(db.String(length=25), nullable=False)
    address = db.Column(db.String(length=255), nullable=False)
    postal_code = db.Column(db.String(length=30), nullable=False)
