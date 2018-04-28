
from project.database import Base, db
# from project.model.insurance import Insurance
# from project.model.item import Item 

insurance_item_junction = db.Table('insurance_item_junction',
    db.Column('insurance_id', db.ForeignKey('insurance.id')),
    db.Column('item_id', db.ForeignKey('item.id'))
)