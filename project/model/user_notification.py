# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db, Base
import datetime

class UserNotification(Base):
    __tablename__ = 'user_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User')

    notification_id = db.Column(db.BigInteger,db.ForeignKey('notifications.id'),nullable=False)
    notification = db.relationship('Notification')

    delivered = db.Column(db.Boolean,default=False)
    seen = db.Column(db.Boolean,default=False)
    send_sms = db.Column(db.Boolean,default=False)

    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return str(self.notification) +" - "+ str(self.user)
