from project.database import db, Base
import datetime
from marshmallow import Schema, fields


class Offer(Base):
    __tablename__ = 'offer'
    id = db.Column(db.BigInteger, primary_key=True)
    offer_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    status = db.Column(db.Integer)
    win = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')
    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item')
    def __str__(self):
        return self.user +" " + self.item + " " + self.offer_price

class OfferSchema(Schema):
    id = fields.Int()
    offer_price = fields.Str()
    date = fields.DateTime()
    status = fields.Int()
    win = fields.Boolean()
    user = fields.Nested('UserSchema',exclude=('offers',))
    item = fields.Nested('ItemSchema',exclude=('offers',))
