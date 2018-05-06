from project.database import db, Base
from marshmallow import Schema, fields

user_product_likes = db.Table('user_product_likes', Base.metadata,
    db.Column('product_id', db.ForeignKey('products.id')),
    db.Column('user_id', db.ForeignKey('users.id'))
)

class LikeSchema(Schema):
    user = fields.Nested("UserSchema")
    product = fields.Nested("ProductSchema")
