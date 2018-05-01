from project.database import db, Base

order_items = db.Table('order_items', Base.metadata,
    db.Column('item_id', db.ForeignKey('items.id')),
    db.Column('order_id', db.ForeignKey('orders.id')),
)
