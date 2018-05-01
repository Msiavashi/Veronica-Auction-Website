from project.database import db, Base

payment_items = db.Table('payment_items', Base.metadata,
    db.Column('payment_id', db.ForeignKey('payments.id')),
    db.Column('item_id', db.ForeignKey('items.id'))
)
