from project.database import db, Base

manufacture_products = db.Table('manufacture_products', Base.metadata,
    db.Column('manufacture_id', db.ForeignKey('manufactures.id')),
    db.Column('product_id', db.ForeignKey('products.id'))
)
