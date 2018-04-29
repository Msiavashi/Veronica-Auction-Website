import datetime
from project.database import Base, db
# from project.model.item import Item
# from project.model.plan import Plan 


class Auction(Base):
    __tablename__ = 'auction'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    minimum_price_increment = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    items = db.relationship('Item')
    plan_id = db.Column(db.BigInteger, db.ForeignKey('plan.id'))
