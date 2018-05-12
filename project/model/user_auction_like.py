from project.database import db, Base
import datetime
from marshmallow import Schema, fields

user_auction_likes = db.Table('user_auction_likes', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)

class LikeAuctionSchema(Schema):
    user = fields.Nested("UserSchema",exclude=('auction_likes',))
    auction = fields.Nested("AuctionSchema",exclude=('likes',))
    date = fields.Str()
