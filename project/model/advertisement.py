from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100),nullable=False)
    description = db.Column(db.Text,nullable=False)
    images = db.Column(db.Text,nullable=False)
    link_title = db.Column(db.String(length=100),nullable=False)
    link = db.Column(db.String(length=255),nullable=False)
    show = db.Column(db.Boolean,default=False)
    discount = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title

class AdvertisementSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    images = fields.Str()
    link_title =fields.Str()
    link =fields.Str()
    show = fields.Boolean()
    discount = fields.Int()
