from project.database import db, Base
from .manufacture_product import manufacture_products
from .manufacture import Manufacture
from .category import Category
from .product_event import product_events
from .user_product_view import user_product_views
from .user_product_like import user_product_likes
from marshmallow import Schema, fields

class Product(Base):

    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    details =  db.Column(db.PickleType, nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category',back_populates='products')
    items = db.relationship('Item')
    comments = db.relationship("Comment")
    events = db.relationship('Event', secondary = product_events, back_populates='products')
    manufacture_id = db.Column(db.BigInteger,db.ForeignKey('manufactures.id'))
    manufacture = db.relationship('Manufacture')
    likes = db.relationship('User', secondary=user_product_likes ,back_populates='likes')
    views = db.relationship('User', secondary=user_product_views ,back_populates='views')
    advertisement = db.relationship('Advertisement' , back_populates ='product')
    def __str__(self):
        return self.name
class ProductSchema(Schema):
    id = fields.Int()
    details = fields.Str()
    quantity = fields.Int()
    review = fields.Str()
    likes = fields.Int()
    details = fields.Raw()
    category = fields.Nested('CategorySchema',exclude=('products',))
    items = fields.Nested('ItemSchema',many=True,exclude=('product',))
    comments = fields.Nested('CommentSchema',many=True,exclude=('product',))
    events = fields.Nested('EventSchema',many=True,exclude=('products',))
    manufacture = fields.Nested('ManufactureSchema',exclude=('products',))
    advertisement = fields.Nested('AdvertisementSchema',exclude=('product',))
    likes = fields.Nested('LikeSchema',many=True,exclude=('likes',))
    views = fields.Nested('ViewSchema',many=True,exclude=('views',))
