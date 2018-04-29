import datetime
from project.database import Base, db
# from project.model.insurance_item_junction import insurance_item_junction
# from project.model.item import Item 


class Insurance(Base):
    __tablename__ = "insurance"
    id = db.Column(db.BigInteger, primary_key=True)
    company_name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item', secondary='insurance_item_junction', back_populates='insurances')
    # insurance_serial = Column(String(100))

