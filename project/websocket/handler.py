# -*- coding: utf-8 -*-
import sys
from importlib import reload
reload(sys)
# sys.setdefaultencoding("utf-8")

from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE

from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime , timedelta
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
<<<<<<< HEAD
=======

>>>>>>> 481f01c
from project.websocket.Timer import timer
import time
from project import socketio
from flask_socketio import emit, join_room, leave_room
<<<<<<< HEAD
=======

>>>>>>> 481f01c

# REDIS_URL = "redis://localhost:6379/0"
# REDIS_CHAN = 'auction'

<<<<<<< HEAD

def get_remained_time(auction_id):
    auction = Auction.query.get(auction_id)

    server_time = datetime.now()
    remained_time = auction.start_date - server_time

    return remained_time



def loadview(data):
    try:
        auction_id = data['auction_id']
        auction = Auction.query.get(auction_id)
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()
        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        for user in users:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price

        user_schema = UserSchema(many=True)
        if(last_offer):
            emit("update_view", {"success":True, "current_offer_price": last_offer.total_price,"users": json.dumps(user_schema.dump(users))})
            return 200
        else:
            emit("update_view", {"success":True , "current_offer_price": 0,"users": json.dumps(user_schema.dump(users))})
            return 200

    except Exception as e:
        emit("failed", {"reason": e.message})
        return 500

=======
>>>>>>> 481f01c
@socketio.on('join')
def join(data):
    print "***************** joined **************"
    room = data['auction_id']
    join_room(room)
    loadview(data)
    emit("join", {"msg": "new client joined auction"}, room=room)

@socketio.on('leave')
def leave(data):
    room = data['room']
    leave_room(room)
    emit("leave", {"msg": "client left room"}, room=room)

#authenticated users only
@socketio.on('bid')
def handle_bid(data):
    if not current_user.is_authenticated:
        emit('unauthorized', {"msg": "login required"})
        return 401

        # is_registered
    try:
        auction_id = data['auction_id']
<<<<<<< HEAD
        user_id = current_user.id
=======
        user_id = data['user_id']
        difference = int(data['difference'])
>>>>>>> 481f01c
        auction = Auction.query.get(auction_id)
        user = current_user
        # check for one minutes remained for starting auction

        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and last_offer.win):
            winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
            user_schema = UserSchema()
            emit("win", {"success": True, "winner": json.dumps(user_schema.dump(winner))}, room=auction_id)
            return 200

        now = datetime.now()
        remained = (auction.start_date - now).seconds
        if(remained > 60):
            emit('failed',{"success":False,"reason":"تا یک دقیقه به شروع حراجی امکان ارسال پیشنهاد وجود ندارد"})
            return 400
        if(remained < 10):
            auction.start_date = now + timedelta(seconds=10)
            db.session.add(auction)
            db.session.commit()

        user_plan = UserPlan.query.filter_by(user_id=user_id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
        my_last_offer = Offer.query.join(UserPlan).filter_by(id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and my_last_offer and my_last_offer.id==last_offer.id):
            emit("failed", {"success":False, "reason":"امکان ارسال پیشنهاد روی پیشنهاد خود را ندارید"})
            return 400

        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1

        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer.current_bids == 0):
            emit("failed", {"success":False,"reason":"پیشنهادات شما به پایان رسید"})
            return 400

        if(last_offer):
            offer.total_price = last_offer.total_price + (BASE_BID_PRICE * auction.ratio)
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
        emit("accepted", {"success": True, "current_bids": offer.current_bids, "total_price": str(offer.total_price) ,"users":json.dumps(user_schema.dump(users))})
        return 200

    except Exception as e:
        emit("error", {"msg": e.message})




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
            emit("auction_done", {"success":True, "winner": json.dumps(user_schema.dump(winner))})
            return 200
        else:
            emit("failed", {"success":False, "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"})
            return 400
    except Exception as e:
        return "{'error':"+str(e)+"}"


@socketio.on('status')
def get_acution_status(data):
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    if (auction.start_date - datetime.now()) <=0:
        auction_done(data)
    else:
        emit("auction_status", {"status": "running"})

        # def get_time(data):
        #     auction_id=data['auction_id']
        #     auction = Auction.query.get(auction_id)
        #     # pretty_time = timer.getCurrentTimerTime(str(auction.start_date))
        #     pretty_time = " "
        #     server_time = datetime.now()
        #     auction_schema = AuctionSchema()
        #     deadline = auction.start_date
        #     now = datetime.now()
        #     remained = (auction.start_date - now)
        #
        #     return '{"auction_deadline":"'+str(remained)+'","auction_id":"'+auction_id+'","token": "'+data['token']+'","success":"true","handler":"get_time","server_time":"'+str(server_time)+'","pretty_time":"'+pretty_time+'"}'
        #         emit("failed", {"reason": e.message})
        #         return 500
