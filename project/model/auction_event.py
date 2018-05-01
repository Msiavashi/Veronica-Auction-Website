from project.database import db, Base

auction_events = db.Table('auction_events', Base.metadata,
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('event_id', db.ForeignKey('events.id')),
    db.Column('discount',db.DECIMAL(precision=20, scale=4))
)
