# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
from marshmallow import Schema, fields
import datetime

class UserMessage(Base):
    __tablename__ = 'user_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))

    title = db.Column(db.String(128), nullable=False)

    # 0 for first and 1 for second
    subject = db.Column(db.Integer, default=0, nullable=False)

    message = db.Column(db.Text, nullable=False)

    file = db.Column(db.String(1024), nullable=True)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " ارسال توسط :" + str(User.query.filter_by(id=self.user_id)) + " درتاریخ " + self.created_at

class UserMessageSchema(Schema):
    id = fields.Int()
    file = fields.Str()
    title = fields.Str()
    create_at = fields.DateTime()
    subject = fields.Str()
    message = fields.Str()
