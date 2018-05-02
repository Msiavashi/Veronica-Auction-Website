from project.database import db, Base

inventory_items = db.Table('inventory_items', Base.metadata,
    db.Column('inventory_id', db.ForeignKey('inventories.id')),
    db.Column('item_id', db.ForeignKey('items.id')),
    db.Column('count',db.Integer())
)
