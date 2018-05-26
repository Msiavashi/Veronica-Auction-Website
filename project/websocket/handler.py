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
from project import socketio
from flask_socketio import emit, join_room, leave_room


@socketio.on('sync_timers')
def sync_timers():
    room = 'index'
    join_room(room)
    now = datetime.now()
    auctions = Auction.query.filter(Auction.start_date >= now).order_by('start_date')
    result = []
    for auction in auctions:
        keyValue = {"auction_id":auction.id,"remained_time":(auction.start_date - now).seconds}
        result.append(keyValue)
    emit("sync_timers",{"timers": result} , room=room)

@socketio.on('join')
def join(data):
    room = data['auction_id']
    join_room(room)
    loadview(data)
    auction = Auction.query.get(data['auction_id'])
    auction_schema = AuctionSchema();
    deadline = (auction.start_date - datetime.now()).seconds
    emit("join",{"msg": "new client joined auction","auction": auction_schema.dump(auction),"deadline":deadline} , room=room)

@socketio.on('leave')
def leave(data):
    room = data['room']
    leave_room(room)
    emit("leave", {"msg": "client left room"}, room=room)

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
            emit("update_view", {"success":True, "current_offer_price": str(last_offer.total_price),"users": user_schema.dump(users)})
        else:
            print "here i am no last_offer"
            emit("update_view", {"success":True , "current_offer_price": 0,"users": user_schema.dump(users)})

    except Exception as e:
        emit("failed", {"reason": e.message})


#authenticated users only
@socketio.on('bid')
def handle_bid(data):
    room=data['auction_id']
    if not current_user.is_authenticated:
        emit('unauthorized', {"msg": "login required"})
        return 401

        # is_registered
    try:
        auction_id = data['auction_id']
        user_id = current_user.id
        auction = Auction.query.get(auction_id)
        user = User.query.get(user_id)
        user_plan = UserPlan.query.filter_by(user_id=user_id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
        auc_part = UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=user_id).first()
        if(not (user_plan and auc_part)):
            emit('failed',{"success":False,"reason":"شما در این حراجی شرکت نکرده اید و مجوز ارسال پیشنهاد ندارید"})
            return 400
        # check for one minutes remained for starting auction

        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and last_offer.win):
            auction_done(data)
            return 200

        now = datetime.now()
        remained = (auction.start_date - now).seconds
        if(remained > 60):
            emit('failed',{"success":False,"reason":"تا یک دقیقه به شروع حراجی امکان ارسال پیشنهاد وجود ندارد"})
            return 400

        my_last_offer = Offer.query.join(UserPlan).filter_by(id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()

        if(last_offer and my_last_offer and my_last_offer.id==last_offer.id):
            emit("failed", {"success":False, "reason":"امکان ارسال پیشنهاد روی پیشنهاد خود را ندارید"})
            return 400

        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1

        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer):
            if(my_last_offer.current_bids > 0):
                offer.total_price = auction.base_price + offer_count * (BASE_BID_PRICE * auction.ratio)
                offer.current_bids = my_last_offer.current_bids - 1
            else:
                emit("failed", {"success":False,"reason":"پیشنهادات شما به پایان رسید"})
                return 400
        elif(last_offer):
            offer.total_price = last_offer.total_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1
        else:
            offer.total_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1

        db.session.add(offer)
        db.session.commit()

        if(remained < 10):
            auction.start_date = now + timedelta(seconds=11)
            db.session.add(auction)
            db.session.commit()

        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        for user in users:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('total_price DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price

        user_schema = UserSchema(many=True)
        emit("accepted", {"success": True, "current_bids": offer.current_bids, "total_price": str(offer.total_price) ,"users":user_schema.dump(users)},room=room)
        return 200

    except Exception as e:
        emit("failed", {"success":False,"reason": e.message})


def auction_done(data):
    room=data['auction_id']
    try:
        auction_id = data['auction_id']
        auction = Auction.query.get(auction_id)
        price = auction.item.price

        total_bids = Offer.query.filter_by(auction_id=auction_id).count()
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('total_price DESC').first()
        if(last_offer):
            last_offer.win = True
            db.session.add(last_offer)
            db.session.commit()
            winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
            user_schema = UserSchema()
            price -= last_offer.total_price
            emit("auction_done", {"success":True, "winner": json.dumps(user_schema.dump(winner)),"discount":str(price)},room=room)
            return 200
        else:
            emit("auction_done", {"success":False, "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"},room=room)
            return 400
    except Exception as e:
        return "{'error':"+str(e)+"}"


@socketio.on('status')
def get_acution_status(data):
    room = data['auction_id']
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    remained = (auction.start_date - datetime.now()).seconds
    server_time = datetime.now()
    auction_time = auction.start_date
    if (int(auction.start_date < datetime.now()) ):
        auction_done(data)
    else:
        emit("auction_status", {"status": "running","remained":remained,"server_time":str(server_time),"auction_time":str(auction_time)},room=room)
