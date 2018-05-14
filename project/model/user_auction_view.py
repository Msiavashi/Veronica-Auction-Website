from project.database import db, Base
from marshmallow import Schema, fields
import datetime


user_auction_views = db.Table('user_auction_views', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('count',db.Integer()),
    db.Column('ip',db.String(length=50)),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)
class ViewAuctionSchema(Schema):
    user = fields.Nested("UserSchema",exclude=('auction_views',))
    auction = fields.Nested("AuctionSchema",exclude=('views',))
    count = fields.Int()
    ip = fields.Str()
    date = fields.Str()
