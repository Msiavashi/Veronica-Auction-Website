from project.database import db, Base

user_product_likes = db.Table('user_product_likes', Base.metadata,
    db.Column('product_id', db.ForeignKey('products.id')),
    db.Column('user_id', db.ForeignKey('users.id'))
)
