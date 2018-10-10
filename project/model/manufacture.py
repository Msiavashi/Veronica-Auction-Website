from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class Manufacture(Base):
    __tablename__ = 'manufactures'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    country = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    details =  db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.name

class ManufactureSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    country = fields.Str()
    description = fields.Str()
    details = fields.Str()
