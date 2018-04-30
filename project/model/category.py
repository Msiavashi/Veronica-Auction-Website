import datetime

from project.database import Base, db


class Category(Base):
    __tablename__ = 'category'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=30))
    categories = db.relationship('Category', remote_side=[id])
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'))
    products = db.relationship('Product', lazy='subquery')
