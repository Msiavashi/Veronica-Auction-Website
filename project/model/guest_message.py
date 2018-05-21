# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class GuestMessage(Base):
    __tablename__ = 'guest_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    full_name = db.Column(db.String(128), nullable=False)

    email = db.Column(db.String(128), nullable=False)

    website = db.Column(db.String(256), nullable=True)

    message = db.Column(db.String(1024), required=True)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " ارسال توسط :" + str(self.full_name) + " درتاریخ " + self.created_at

# class GuestMessageSchema(Schema):
#     id = fields.Int()
#     file = fields.Str()
#     title = fields.Str()
#     create_at = fields.DateTime()
#     subject = fields.Str()
#     message = fields.Str()
