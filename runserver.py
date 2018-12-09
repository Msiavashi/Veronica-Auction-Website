#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, socketio
from project.database import *
from project.admin import admin
import time
import datetime
from project.model import Auction,AuctionNotification,UserAuctionNotification

# from project.cron import cron
# from project.cron import auction_reminder

def background():
    print 'background'
    while True:
        now = datetime.datetime.now()
        auctions = Auction.query.filter(Auction.start_date > now).order_by("start_date").all()
        for auction in auctions:
            remained = (auction.start_date - now).seconds
            print 'remained',remained
            if remained ==0:
                acn = AuctionNotification()
                acn.title = "اطلاع رسانی اتمام  حراجی : " + auction.title
                acn.text = "جهت اطلاع شما کاربر گرامی حراجی "\
                +"\n"+ auction.title\
                +"\n"+ "به اتمام رسید"
                acn.link = "/auction/view/"+str(auction.id)
                acn.auction = auction
                db.session.add(acn)
                db.session.commit()
            if (remained <= 300 and not AuctionNotification.query.filter_by(auction_id=auction.id).first()):
                acn = AuctionNotification()
                acn.title = " اطلاع رسانی شروع حراجی : " + auction.title
                acn.text = "جهت اطلاع شما کاربر گرامی حراجی "\
                +"\n"+ auction.title\
                +"\n"+ "تا ۵ دقیقه دیگر آغاز خواهد شد."
                acn.link = "/auction/view/"+str(auction.id)
                acn.auction = auction
                db.session.add(acn)
                db.session.commit()
        socketio.sleep(1)

def sms_sender():
    print 'sms_sender'
    while True:
        recipients = UserAuctionNotification.query.filter_by(delivered=False).all()
        for recipient in recipients:
            print "sms sent to :",str(recipient.user)
            recipient.delivered = True
            db.session.add(recipient)
            db.session.commit()
        socketio.sleep(1)

def notification_cleaner():
    print 'notification_cleaner'
    while True:
        UserAuctionNotification.query.filter_by(delivered=True,seen=True).delete()
        db.session.commit()
        socketio.sleep(300)


socketio.start_background_task(background)
socketio.start_background_task(sms_sender)
socketio.start_background_task(notification_cleaner)

if __name__ == '__main__':
    # production
    # port = int(os.environ.get("PORT", 8000))
    # app.debug = False
    # try:
    #     socketio.run(app, port=port, debug=False)
    # except socket.error as socketerror:
    #     print("Error: ", socketerror)

    # developement
    port = int(os.environ.get("PORT", 9001))
    app.debug = True
    socketio.run(app, port=port, debug=True)
