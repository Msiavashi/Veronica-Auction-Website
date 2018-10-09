# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Comment(Base):
    __tablename__ = 'comments'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')
    
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
     updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title + " متن پیام :" + self.message

class CommentSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    message = fields.Str()
    likes = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user = fields.Nested('UserSchema',exclude=('comments',))
    product = fields.Nested('ProductSchema',exclude=('products',))
