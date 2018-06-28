from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Category(Base):
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=255),nullable=False)
    icon = db.Column(db.Text)

    categories = db.relationship('Category', remote_side=[id])

    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category')

    products = db.relationship('Product', back_populates = 'category')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return self.title

class CategorySchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    icon = fields.Str()
    # products = fields.Nested('ProductSchema', many=True ,exclude=('category', ))
    # categories = fields.Nested('self', many=True,exclude=('categories', ))
