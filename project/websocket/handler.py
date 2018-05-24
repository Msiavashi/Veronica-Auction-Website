# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE

from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime , timedelta
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from project.websocket.Timer import timer
import time

@login_required
def offer_bid(data):
    try:
        auction_id = data['auction_id']
        user_id = data['user_id']
        difference = int(data['difference'])
        auction = Auction.query.get(auction_id)
        user = User.query.get(user_id)

        # check for one minutes remained for starting auction

        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and last_offer.win):
            winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
            user_schema = UserSchema()
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"auction_done","winner":'+json.dumps(user_schema.dump(winner))+'}'

        now = datetime.now()
        remained = (auction.start_date - now).seconds
        if(remained > 60 * 10):
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"false","reason":"تا یک دقیقه به شروع حراجی امکان ارسال پیشنهاد وجود ندارد","user_id":"'+str(user_id)+'"}'
        if(remained < 10 * 58):
            auction.start_date = datetime.now() + timedelta(seconds=10)
            db.session.add(auction)
            db.session.commit()

        user_plan = UserPlan.query.filter_by(user_id=user_id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
        my_last_offer = Offer.query.join(UserPlan).filter_by(id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and my_last_offer and my_last_offer.id==last_offer.id):
            return '{"auction_id":"'+ auction_id +'","token":"'+ data['token'] +'","success":"false","reason":"امکان ارسال پیشنهاد روی پیشنهاد خود را ندارید","user_id":"'+user_id+'"}'

        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1

        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer):
            if(my_last_offer.current_bids > 0):
                offer.total_price = auction.base_price + offer_count * (BASE_BID_PRICE * auction.ratio)
                offer.current_bids = my_last_offer.current_bids - 1
            else:
                return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"false","reason":"پیشنهادات شما به پایان رسید"}'
        elif(last_offer):
            offer.total_price = last_offer.total_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1
        else:
            offer.total_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1


        db.session.add(offer)
        db.session.commit()

        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        for user in users:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price

        user_schema = UserSchema(many=True)
        remained = (auction.start_date - now).seconds
        remained_time = (auction.start_date - datetime.now()).seconds * 1000
        if(remained < 10):
            remained_time = 10 * 1000

        return '{"auction_id":"'+auction_id+'","handler":"offer","token": "'+data['token']+'","success":"true","current_bids":"'+str(offer.current_bids)+'","user_id":"'+str(user_id)+'","remained_time":'+str(remained_time)+',"total_price":'+str(offer.total_price)+',"users":'+json.dumps(user_schema.dump(users))+'}'

    except Exception as e:
        return "{'error':"+str(e)+"}"

def loadview(data):
    try:
        auction_id = data['auction_id']
        auction = Auction.query.get(auction_id)
        remained_time = (auction.start_date - datetime.now()).seconds * 1000
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()
        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        for user in users:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price

        user_schema = UserSchema(many=True)
        if(last_offer):
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"loadview","current_offer_price":"'+ str(last_offer.total_price) +'","users":'+json.dumps(user_schema.dump(users))+',"remained_time":'+str(remained_time)+'}'
        else:
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"loadview","current_offer_price":"0" ,"users":'+json.dumps(user_schema.dump(users))+', "remained_time":'+str(remained_time)+'}'

    except Exception as e:
        return "{'error':"+str(e)+"}"

def auction_done(data):
    try:
        auction_id = data['auction_id']
        total_bids = Offer.query.filter_by(auction_id=auction_id).count()
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()
        if(last_offer):
            last_offer.win = True
            db.session.add(last_offer)
            db.session.commit()
            winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
            user_schema = UserSchema()
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"auction_done","winner":'+json.dumps(user_schema.dump(winner))+'}'
        else:
            return '{"auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"false","handler":"auction_done" , "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"}'
    except Exception as e:
        return "{'error':"+str(e)+"}"

def get_time(data):
    auction_id=data['auction_id']
    auction = Auction.query.get(auction_id)
    # pretty_time = timer.getCurrentTimerTime(str(auction.start_date))
    pretty_time = " "
    server_time = datetime.now()
    auction_schema = AuctionSchema()
    deadline = auction.start_date
    return '{"auction_deadline":"'+str(deadline)+'","auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"get_time","server_time":"'+str(server_time)+'","pretty_time":"'+pretty_time+'"}'
