from project.database import db, Base
from marshmallow import Schema, fields

class Category(Base):
    db.relationshipS_TO_DICT = True
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=255))
    icon = db.Column(db.String(length=255))
    categories = db.relationship('Category', remote_side=[id])
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    products = db.relationship('Product', back_populates = 'category')
    def __str__(self):
        return self.name

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    icon = fields.Str()
    products = fields.Nested('ProductSchema', many=True ,exclude=('category', ))
    categories = fields.Nested('self', many=True)
