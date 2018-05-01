from project.database import db, Base
import datetime


class ProductEvent(Base):

    __tablename__ = 'product_events'
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    products = db.relationship('Product')
    discount = db.Column(db.DECIMAL(precision=20, scale=4))
