from project.database import db, Base
import datetime
from comment import Comment
from address import Address
from payment import Payment
from order import Order
from user_plan import user_plans
from user_gift import user_gifts
from user_role import user_roles
from user_auction import user_auctions
from product import Product
from user_product_view import user_product_views
from user_product_like import user_product_likes
from marshmallow import Schema, fields

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(length=255), nullable=False)
    first_name = db.Column(db.String(length=100))
    last_name = db.Column(db.String(length=100))
    work_place = db.Column(db.String(length=100))
    mobile = db.Column(db.String(length=15), nullable=False)
    email = db.Column(db.String(length=255))
    password = db.Column(db.String(length=100), nullable=False)

    #please check for dafault avatar address from config file
    avatar = db.Column(db.String(length=300))

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    #credit for each user
    credit = db.Column(db.DECIMAL(precision=20, scale=4), default=0)

    comments = db.relationship('Comment')
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    # address = db.relationship('Address')
    payments = db.relationship('Payment')
    orders = db.relationship('Order')
    likes = db.relationship('Product', secondary=user_product_likes ,back_populates='likes')
    views = db.relationship('Product', secondary=user_product_views ,back_populates='views')
    roles = db.relationship('Role',secondary=user_roles,back_populates='users')
    plans = db.relationship('Plan', secondary=user_plans, back_populates='users')
    gifts = db.relationship('Gift', secondary=user_gifts, back_populates='users')
    auctions = db.relationship('Auction', secondary=user_auctions,back_populates='users')


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    # password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    work_place = fields.Str()
    mobile = fields.Str()
    email = fields.Email()
    credit = fields.Decimal()
    address_id = fields.Int()

    payments = fields.Nested('PaymentSchema', many=True)
    orders = fields.Nested('OrderSchema', many=True)
    likes = fields.Nested('LikeSchema', many=True)
    views = fields.Nested('ViewSchema', many=True)
    roles = fields.Nested('RoleSchema', many=True)
    plans = fields.Nested('PlanSchema', many=True)
    gifts = fields.Nested('GiftSchema', many=True)
    auctions = fields.Nested('AuctionSchema', many=True)