from project.database import db, Base
import datetime

user_auctions = db.Table('user_auctions', Base.metadata,
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('date',db.TIMESTAMP,default=datetime.datetime.now)
)
