from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Event(Base):
    __tablename__ = 'events'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255),nullable=False)
    description = db.Column(db.Text,nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    is_active = db.Column(db.Boolean,default=False)
    discount = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    def __str__(self):
        return self.title

class EventSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    is_active = fields.Boolean()
    discount = fields.Int()
