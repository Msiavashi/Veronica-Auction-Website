import datetime
from project.database import Base, db, ma
from project.model.order import Order 
# from project.model.item import Item 

class Offer(Base):
    __tablename__ = 'offer'
    id = db.Column(db.BigInteger, primary_key=True)
    offer_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'))
    item_id = db.Column(db.BigInteger, db.ForeignKey('item.id'))

class OfferSchema(ma.ModelSchema):
    class Meta:
        model = Offer 