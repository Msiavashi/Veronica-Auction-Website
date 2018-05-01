from project.database import db, Base
import datetime

user_product_views = db.Table('user_product_views', Base.metadata,
    db.Column('product_id', db.ForeignKey('products.id')),
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('ip_address',db.String(length=64)),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)
