from project.database import db, Base
import datetime
from user import User

class Offer(Base):
    __tablename__ = 'offer'
    id = db.Column(db.BigInteger, primary_key=True)
    offer_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')
    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item')
    win = db.Column(db.Boolean,default=False)
