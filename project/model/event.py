from project.database import db, Base
import datetime
from auction_event import auction_events
from product_event import product_events


class Event(Base):

    __tablename__ = 'events'
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4))
    auctions = db.relationship('Auction', secondary = auction_events, back_populates='events')
    products = db.relationship('Product', secondary = product_events, back_populates='events')
