from project.database import db, Base
from insurance_item import insurance_items

class Insurance(Base):
    __tablename__ = "insurances"
    id = db.Column(db.BigInteger, primary_key=True)
    company_name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item', secondary=insurance_items, back_populates='insurances')
