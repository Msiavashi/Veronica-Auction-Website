from project.database import db, Base
from marshmallow import Schema, fields

class Product(Base):

    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    details = db.Column(db.PickleType, nullable=True)
    # product images link
    images = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products')
    items = db.relationship('Item')
    comments = db.relationship("Comment")
    events = db.relationship('Event', secondary = 'product_events', back_populates='products')
    manufacture_id = db.Column(db.BigInteger,db.ForeignKey('manufactures.id'))
    manufacture = db.relationship('Manufacture')
    likes = db.relationship('User', secondary='user_product_likes' ,back_populates='product_likes')
    views = db.relationship('User', secondary='user_product_views' ,back_populates='product_views')
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
    images = fields.Raw()
    category = fields.Nested('CategorySchema',exclude=('products',))
    items = fields.Nested('ItemSchema',many=True,exclude=('product',))
    comments = fields.Nested('CommentSchema',many=True,exclude=('product',))
    events = fields.Nested('EventSchema',many=True,exclude=('products',))
    manufacture = fields.Nested('ManufactureSchema',exclude=('products',))
    advertisement = fields.Nested('AdvertisementSchema',exclude=('product',))
    likes = fields.Nested('LikeProductSchema',many=True,exclude=('likes',))
    views = fields.Nested('ViewProductSchema',many=True,exclude=('views',))
