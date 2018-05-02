from project.database import db, Base
from marshmallow import Schema, fields

class Category(Base):
    db.relationshipS_TO_DICT = True
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=255))
    categories = db.relationship('Category', remote_side=[id])
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    products = db.relationship('Product', back_populates = 'category')


class CategorySchema(Schema):
    id = fields.Int()
    description = fields.Str()
    products = fields.Nested('ProductSchema', many=True)
    categories = fields.Nested('CategorySchema')
