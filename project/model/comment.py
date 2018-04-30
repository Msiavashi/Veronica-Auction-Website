
import datetime

from project.database import Base, db


class Comment(Base):
    __tablename__ = 'comment'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    message = db.Column(db.String(length=2048), nullable=False)
    stars = db.Column(db.Integer, default=0)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'))
    