# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime
import enum
from . import User


class UserMessage(Base):
    __tablename__ = 'user_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user = db.relationship('User')

    message = db.Column(db.String(1024), nullable=True)

    title = db.Column(db.String(128), nullable=True)

    subject = db.Column(db.String(512), nullable=False)

    file = db.Column(db.String(1024), nullable=True)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return " ارسال توسط : " +  str(self.user.username) + " با عنوان : " + self.title + " درتاریخ : " + str(self.created_at) 
        except Exception as e:
            return self.title


class UserMessageSchema(Schema):
    id = fields.Int()
    file = fields.Str()
    title = fields.Str()
    create_at = fields.DateTime()
    subject = fields.Str()
    message = fields.Str()
