from project.database import db, Base
import datetime


class AuctionEvent(Base):

    __tablename__ = 'auction_events'
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    auctions = db.relationship('Auction')
    discount = db.Column(db.DECIMAL(precision=20, scale=4))
