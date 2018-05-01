from project.database import db, Base

product_events = db.Table('product_events', Base.metadata,
    db.Column('product_id', db.ForeignKey('products.id')),
    db.Column('event_id', db.ForeignKey('events.id')),
    db.Column('discount',db.DECIMAL(precision=20, scale=4))
)
