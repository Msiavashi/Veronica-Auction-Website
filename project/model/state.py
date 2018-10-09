# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class State(Base):
    __tablename__ = 'states'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
     updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title

class StateSchema(Schema):
    id = fields.Int()
    title = fields.Str()
