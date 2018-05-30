from project.database import db, Base
from marshmallow import Schema, fields
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask_login import UserMixin
from . import Role

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
    alias_name = db.Column(db.String(128), nullable = True)
    first_name = db.Column(db.String(length=100))
    last_name = db.Column(db.String(length=100))
    work_place = db.Column(db.String(length=100))
    mobile = db.Column(db.String(length=15), nullable=False)
    email = db.Column(db.String(length=255))
    password = db.Column(db.String(length=100), nullable=False)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)


    invitor = db.Column(db.String(length=255))

    credit = db.Column(db.DECIMAL(precision=20, scale=4), default=0)

    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address', uselist=False, back_populates='user')

    comments = db.relationship('Comment')

    avatar = db.Column(db.Text,default="['001.png']") #avatar path

    user_plans = db.relationship('UserPlan')

    payments = db.relationship('Payment')

    messages = db.relationship('UserMessage')

    orders = db.relationship('Order')

    # offers = db.relationship('Offer')

    roles = db.relationship('Role' , secondary = 'user_roles', back_populates='users')

    gifts = db.relationship('Gift', secondary='user_gifts', back_populates='users',lazy='dynamic')

    auctions = db.relationship('Auction', lazy='dynamic', secondary='user_auction_participations',back_populates='participants')

    auction_views = db.relationship('Auction', secondary ='user_auction_views', back_populates='views')
    auction_likes = db.relationship('Auction', secondary ='user_auction_likes', back_populates='likes')

    def __str__(self):
        if(self.first_name and self.last_name):
            return str(self.first_name) + " " + str(self.last_name)
        elif (self.alias_name):
            return str(self.alias_name)
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

    def is_admin(self):
        admin = False
        for role in self.roles:
            if( role.name == 'admin' ):
                admin = True
        return admin

    def has_auction(self,id):
        try:
            return next(a for a in self.auctions if a.id == id),None
        except Exception as e:
            return None

    def has_role(self,name):
        try:
            return next(a for a in self.roles if a.name == name),None
        except Exception as e:
            return None

    def save_to_db(self):
        #add default role to created user
        role = Role.query.get(2)
        self.roles.append(role)
        db.session.add(self)
        db.session.commit()

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    alias_name = fields.Str()
    # password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    work_place = fields.Str()
    mobile = fields.Str()
    email = fields.Email()
    credit = fields.Str()
    avatar = fields.Str()
    invitor = fields.Str()
    current_bids = fields.Str()
    current_offer_price = fields.Str()

    address = fields.Nested('AddressSchema')
    comments = fields.Nested('CommentSchema', many=True,exclude=('user',))
    payments = fields.Nested('PaymentSchema', many=True,exclude=('user',))
    offers = fields.Nested('OfferSchema', many=True,exclude=('user',))
    orders = fields.Nested('OrderSchema', many=True,exclude=('user',))
    roles = fields.Nested('RoleSchema',many=True,exclude=('users',))
    plans = fields.Nested('PlanSchema', many=True,exclude=('users',))
    gifts = fields.Nested('GiftSchema', many=True,exclude=('users',))
    auctions = fields.Nested('AuctionSchema', many=True,exclude=('participants',))
    user_plans = fields.Nested('UserPlanSchema', many=True,exclude=('user',))

    auction_likes = fields.Nested('LikeAuctionSchema',many=True,exclude=('user',))
    auction_views = fields.Nested('ViewAuctionSchema', many=True,exclude=('user',))
    product_likes = fields.Nested('LikeProductSchema',many=True,exclude=('user',))
    product_views = fields.Nested('ViewProductSchema', many=True,exclude=('user',))
