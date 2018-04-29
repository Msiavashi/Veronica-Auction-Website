from project.database import Base
from project.database import db 

manufacture_product_junction = db.Table('manufacture_product_junction',
    db.Column('manufacture_id', db.ForeignKey('manufacture.id')),
    db.Column('product_id', db.ForeignKey('product.id'))
)


