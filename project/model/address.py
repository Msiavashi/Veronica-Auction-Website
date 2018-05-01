from project.database import db, Base

class Address(Base):
    __tablename__ = 'addresses'
    id = db.Column(db.BigInteger, primary_key=True)
    country = db.Column(db.String(length=50),nullable=True)
    state = db.Column(db.String(length=50), nullable=False)
    city = db.Column(db.String(length=50), nullable=False)
    address = db.Column(db.String(length=255), nullable=False)
    postal_code = db.Column(db.String(length=20), nullable=False)
