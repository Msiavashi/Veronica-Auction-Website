# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
import datetime

class Notification(Base):
    __tablename__ = 'notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(length=1024))
    users = db.relationship('User', secondary='user_notifications', back_populates='notifications',lazy='dynamic',single_parent=True,cascade="all, delete-orphan")

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
