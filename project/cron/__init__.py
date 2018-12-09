# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from crontab import CronTab
import os

cron = CronTab(user='user')
cron.remove_all()
current_path = os.path.dirname(os.path.abspath(__file__))

def test():
    job = cron.new(command='python '+current_path+'/test.py')
    job.minute.every(1)
    cron.write()
    print job.is_valid()
    for job in cron:
        print job

def auctions():
    job = cron.new(command='python '+current_path+'/auction_reminder.py')
    job.minute.every(1)
    cron.write()
    print job.is_valid()
    for job in cron:
        print job

# test()
auctions()

# import schedule
# import time
# from datetime import datetime
# from project.model import *
#
# def deamon():
#     print("I'm working on auctions...")
#     now = datetime.now()
#     auction = Auction.query.filter(Auction.start_date > now).order_by("start_date").first()
#     remained = (auction.start_date - datetime.now()).minutes
#     if (remained <= 5):
#         acn = AuctionNotification()
#         acn.title = "اطلاع رسانی شروع حراجی" + auction.title
#         acn.text = "جهت اطلاع شما کاربر گرامی حراجی " + auction.title + "تا ۵ دقیقه دیگر آغاز خواهد شد."
#         acn.link = "/auction/view/"+auction.id
#         acn.auction = auction
#
#
# schedule.every(5).seconds.do(deamon)
# # schedule.every().hour.do(job)
# # schedule.every().day.at("00:00").do(deamon)
# while 1:
#     schedule.run_pending()
#     time.sleep(1)
