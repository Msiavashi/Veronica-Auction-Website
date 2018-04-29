import datetime
from project.database import Base, db
# from project.model.category import Category 
# from project.model.comment import Comment
# from project.model.item import Item
# from project.model.manufacture_product_junction import manufacture_product_junction
# from project.model.manufacture import Manufacture


class Product(Base):

    __tablename__ = 'product'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    total_available = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    stars = db.Column(db.Integer, default=0)
    details =  db.Column(db.PickleType, nullable=True)
    items = db.relationship('Item')
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'))
    comments = db.relationship("Comment")
    # state = Column("String", )sadasd
    manufactures = db.relationship('Manufacture', secondary='manufacture_product_junction', back_populates='products')

    