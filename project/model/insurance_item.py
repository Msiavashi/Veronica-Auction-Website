from project.database import db, Base

insurance_items = db.Table('insurance_items', Base.metadata,
    db.Column('insurance_id', db.ForeignKey('insurances.id')),
    db.Column('item_id', db.ForeignKey('items.id'))
)
