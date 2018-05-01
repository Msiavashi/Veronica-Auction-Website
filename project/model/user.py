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
from user_product_view import user_product_views
from user_product_like import user_product_likes

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
    address = db.relationship('Address')
    payments = db.relationship('Payment')
    orders = db.relationship('Order')
    likes = db.relationship('Product', secondary=user_product_likes ,back_populates='products')
    views = db.relationship('Product', secondary=user_product_views ,back_populates='products')
    roles = db.relationship('Role',secondary=user_roles,back_populates='users')
    plans = db.relationship('Plan', secondary=user_plans, back_populates='users')
    gifts = db.relationship('Gift', secondary=user_gifts, back_populates='users')
    auctions = db.relationship('Auction', secondary=user_auctions,back_populates='users')
