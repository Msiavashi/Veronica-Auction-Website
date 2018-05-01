from project.database import db, Base
import datetime
from item import Item
from event import Event
from user_auction import user_auctions
from auction_event import auction_events

class Auction(Base):
    __tablename__ = 'auctions'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    register_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    minimum_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    maximum_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_members = db.Column(db.BigInteger,default=40)
    item = db.relationship('Item')
    users = db.relationship('User',secondary = user_auctions,back_populates='auctions')
    events = db.relationship('Event', secondary = auction_events, back_populates='auctions')
