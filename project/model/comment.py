
from project.database import db, Base
import datetime
from product import Product
from marshmallow import Schema, fields

class Comment(Base):
    __tablename__ = 'comments'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    message = db.Column(db.String(length=2048), nullable=False)
    likes = db.Column(db.Integer, default=0)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')


class CommentSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    message = fields.Str()
    likes = fields.Int()
    date = fields.DateTime()
    user = fields.Nested('UserSchema')
    product = fields.Nested('ProductSchema')
