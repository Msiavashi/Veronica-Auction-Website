from passlib.hash import pbkdf2_sha256 as sha256
from project.database import db, Base
from flask_login import UserMixin
import datetime
from marshmallow import Schema, fields
from .user_auction_view import user_auction_views
from .user_auction_like import user_auction_likes

class User(Base,UserMixin):
    def __init__(self, username):
        try:
             return cls.query.get(uid)
        except:
         return None

    __tablename__ = 'users'
    __table_args__ = (db.UniqueConstraint('username', name='users_username_uc'),)

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

    invitor = db.Column(db.String(length=255))

    #credit for each user
    credit = db.Column(db.DECIMAL(precision=20, scale=4), default=0)

    comments = db.relationship('Comment')
    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address')
    payments = db.relationship('Payment')
    orders = db.relationship('Order')


    roles = db.relationship('Role',secondary='user_roles',back_populates='users')
    plans = db.relationship('Plan', secondary='user_plans', back_populates='users')
    gifts = db.relationship('Gift', secondary='user_gifts', back_populates='users')
    auctions = db.relationship('Auction', secondary='user_auctions',back_populates='participants')

    product_likes = db.relationship('Product', secondary='user_product_likes' ,back_populates='likes')
    product_views = db.relationship('Product', secondary='user_product_views' ,back_populates='views')

    auction_views = db.relationship('Auction', secondary ='user_auction_views', back_populates='views')
    auction_likes = db.relationship('Auction', secondary ='user_auction_likes', back_populates='likes')

    def __str__(self):
        if(self.first_name):
            return (str(self.first_name) + " " + str(self.last_name))
        else: return self.username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    # password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    work_place = fields.Str()
    mobile = fields.Str()
    email = fields.Email()
    credit = fields.Str()
    address_id = fields.Int()
    avatar = fields.Str()
    payments = fields.Nested('PaymentSchema', many=True,exclude=('users',))
    orders = fields.Nested('OrderSchema', many=True,exclude=('users',))
    roles = fields.Nested('RoleSchema', many=True,exclude=('users',))
    plans = fields.Nested('PlanSchema', many=True,exclude=('users',))
    gifts = fields.Nested('GiftSchema', many=True,exclude=('users',))
    auctions = fields.Nested('AuctionSchema', many=True,exclude=('participants',))

    auction_likes = fields.Nested('LikeAuctionSchema',many=True,exclude=('user',))
    auction_views = fields.Nested('ViewAuctionSchema', many=True,exclude=('user',))
    product_likes = fields.Nested('LikeProductSchema',many=True,exclude=('user',))
    product_views = fields.Nested('ViewProductSchema', many=True,exclude=('user',))
