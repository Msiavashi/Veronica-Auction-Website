# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import datetime
from project.model import *
from project.database import db

print("I'm working on auctions...")
now = datetime.datetime.now()
auction = Auction.query.filter(Auction.start_date > now).order_by("start_date").first()
if auction:
    remained = (auction.start_date - now).seconds
    if (remained <= 300):
        acn = AuctionNotification()
        acn.title = " اطلاع رسانی شروع حراجی : " + auction.title
        acn.text = "جهت اطلاع شما کاربر گرامی حراجی "\
        +"\n"+ auction.title\
        +"\n"+ "تا ۵ دقیقه دیگر آغاز خواهد شد."
        acn.link = "/auction/view/"+str(auction.id)
        acn.auction = auction
        db.session.add(acn)
        db.session.commit()
