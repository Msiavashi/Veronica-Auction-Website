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
from flask_jwt_extended import jwt_required
from sqlalchemy import or_ , and_


@socketio.on('sync_carts_join')
def sync_carts_join(data):
    room = data['room']
    join_room(room)
    emit("sync_carts_join" , room=room)
    return 200

@socketio.on('sync_timers_join')
def sync_timers_join(data):
    room = data['room']
    join_room(room)
    emit("sync_timers_join" , room=room)
    return 200

@socketio.on('sync_carts')
def sync_carts(data):
    room = data['room']
    if current_user.is_authenticated:
        result = Order.query.filter(or_(Order.status==OrderStatus.UNPAID, Order.status==OrderStatus.PAYING)).filter_by(user_id=current_user.id).order_by('created_at DESC')
        orders = []
        for order in result:
            title = order.item.product.title
            if (len(title) > 20):
                title = title[:20]+"..."
            item_title = order.item.title
            if (len(item_title) > 50):
                item_title = item_title[:50]+"..."
            product_title = order.item.product.title
            if (len(product_title) > 50):
                product_title = product_title[:50]+"..."
            fulltitle = product_title + " - " + item_title
            discounted_price = 0

            if order.discount_status == OrderDiscountStatus.REGULAR:
                discounted_price = order.item.discount * order.total

            elif order.discount_status == OrderDiscountStatus.INAUCTION :
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                discounted_price = auctionplan.discount

            elif order.discount_status == OrderDiscountStatus.AUCTIONWINNER:
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                offer = Offer.query.filter_by(win=True).join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                discounted_price = order.item.price - offer.total_price

            orders.append({
            "id" : order.id,
            "item_id" : order.item.id,
            "title" : title,
            "item_title" : item_title,
            "product_title" : product_title,
            "fulltitle" : product_title + " - " + item_title,
            "images" : order.item.images,
            "main_price" : str(order.total * order.item.price),
            "discounted_price" : str(order.total * order.item.price - discounted_price),
            "quantity" : order.item.quantity,
            "total" : order.total,
            "status" : order.status,
            "discount_status" : order.discount_status,
            })

        emit("sync_carts",orders , room=room)
    else:
        if "orders" in session:
            emit("sync_carts", session['orders'] , room=room)
        else:
            emit("sync_carts",[] , room=room)


@socketio.on('sync_timers')
def sync_timers(data):
    room = data['room']
    now = datetime.now()
    results = Auction.query.all()
    auctions=[]
    for auction in results:
        if((auction.start_date - now).days == 0) :
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            remained_time = (auction.start_date - now).seconds
            auctions.append({
            "id":auction.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            "max_price":str(auction.max_price),
            "main_price":str(auction.item.price),
            "remained_time":remained_time,
            "participants":auction_participants,
            "max_members":auction.max_members,
            'expired':now > auction.start_date,
            })

    emit("sync_timers",{"auctions": auctions} , room=room)

@socketio.on('join')
def join(data):
    room = data['auction_id']
    join_room(room)
    loadview(data)
    auction = Auction.query.get(data['auction_id'])
    auction_schema = AuctionSchema();
    deadline = (auction.start_date - datetime.now()).seconds + 1
    emit("join",{"msg": "new client joined auction","auction": auction_schema.dump(auction),"deadline":deadline} , room=room)

@socketio.on('leave_auction')
def leave_auction(data):
    room = data['auction_id']
    emit("leave_auction", {"message": "client left room"}, room=room)
    leave_room(room)
    print 'leaving room',room
    return 200

def loadview(data):
    try:
        auction_id = data['auction_id']
        # auction = Auction.query.get(auction_id)
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
            current_bids = user_last_offer.current_bids
            current_offer_price = user_last_offer.total_price
            pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
            users.append({
                "current_bids" : current_bids,
                "current_offer_price" : int(current_offer_price),
                "pretty_name" : pretty_name ,
                "avatar" : user.avatar,
                "id": user.id
            })

        if(last_offer):
            emit("update_view", {"success":True, "current_offer_price": str(last_offer.total_price),"users": users})
        else:
            emit("update_view", {"success":True , "current_offer_price": 0,"users": users})

    except Exception as e:
        emit("failed", {"reason": e.message})


#authenticated users only
@socketio.on('bid')
def bid(data):
    room=data['auction_id']
    if not current_user.is_authenticated:
        emit('unauthorized', {"msg": "login required"})
        return 401
        # is_registered
    try:
        auction_id = data['auction_id']
        user_id = current_user.id
        auction = Auction.query.get(auction_id)

        if(auction.start_date < datetime.now()):
            emit('failed',{"success":False,"reason":"وقت شرکت در حراجی به اتمام رسیده است"})
            return 400
        user = User.query.get(user_id)
        user_plan = UserPlan.query.filter_by(user_id=user_id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
        auc_part = UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=user_id).first()
        if(not (user_plan and auc_part)):
            emit('failed',{"success":False,"reason":"شما در این حراجی شرکت نکرده اید و مجوز ارسال پیشنهاد ندارید"})
            return 400
        # check for one minutes remained for starting auction

        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()

        if(last_offer and last_offer.win):
            auction_done(data)
            return 200

        now = datetime.now()
        remained = (auction.start_date + timedelta(seconds=1) - now).seconds
        if(remained > 60):
            emit('failed',{"success":False,"reason":"تا یک دقیقه به شروع حراجی امکان ارسال پیشنهاد وجود ندارد"})
            return 400

        my_last_offer = Offer.query.join(UserPlan).filter_by(id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()

        if(last_offer and my_last_offer and my_last_offer.id==last_offer.id):
            emit("failed", {"success":False, "reason":"امکان ارسال پیشنهاد روی پیشنهاد خود را ندارید"})
            return 400

        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1

        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer):
            if(my_last_offer.current_bids > 0):
                calculated_price = auction.base_price + offer_count * (BASE_BID_PRICE * auction.ratio)
                if( calculated_price < auction.max_price):
                    offer.total_price = calculated_price
                else:
                    offer.total_price = auction.max_price
                offer.current_bids = my_last_offer.current_bids - 1
            else:
                emit("failed", {"success":False,"reason":"پیشنهادات شما به پایان رسید"})
                return 400
        elif(last_offer):
            #get last_offer price for offer
            offer.total_price = last_offer.total_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1
        else:
            #starting price for first offer
            offer.total_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1

        db.session.add(offer)
        db.session.commit()

        if(remained < 10 and remained > 0):
            auction.start_date = now + timedelta(seconds=11)
            db.session.add(auction)
            db.session.commit()
        elif(remained <=0 ):
            return auction_done(data)

        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
            current_bids = user_last_offer.current_bids
            current_offer_price = user_last_offer.total_price
            pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
            users.append({
                "current_bids" : current_bids,
                "current_offer_price" : int(current_offer_price),
                "pretty_name" : pretty_name ,
                "avatar" : user.avatar,
                "id": user.id
            })

        emit("accepted", {"success": True, "current_bids": offer.current_bids, "total_price": str(offer.total_price) ,"users":users},room=room)
        return 200

    except Exception as e:
        emit("failed", {"success":False,"reason": e.message})

def auction_done(data):
    room = data['auction_id']
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)

    total_bids = Offer.query.filter_by(auction_id=auction_id).count()
    last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()

    if(last_offer):

        last_offer.win = True
        db.session.add(last_offer)
        db.session.commit()

        winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
        print "winner :",winner
        user_schema = UserSchema()
        discounted_price = auction.item.price - last_offer.total_price

        #set the order for winner in he/she's carts

        last_order = Order.query.filter_by(user_id=winner.id,item_id=auction.item.id).first()

        if last_order :
            last_order.total_cost = last_offer.total_price
            last_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
            last_order.total_discount = discounted_price
            last_order.total = 1
            db.session.add(last_order)
            db.session.commit()
        else:
            new_order = Order()
            new_order.user = winner
            new_order.item = auction.item
            new_order.total_cost = last_offer.total_price
            new_order.status = OrderStatus.UNPAID
            new_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
            new_order.total = 1
            new_order.total_discount = discounted_price
            db.session.add(new_order)
            db.session.commit()

        emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": user_schema.dump(winner),"discount":str(discounted_price)},room=room)
        # leave_auction(data)
        return 200
    else:
        emit("auction_done", {"success":False, "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"},room=room)
        # leave_auction(data)
        return 400
    # except Exception as e:
    #     return "{'error':"+str(e)+"}"


@socketio.on('status')
def get_acution_status(data):
    room = data['auction_id']
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    remained = (auction.start_date - datetime.now()).seconds
    server_time = datetime.now()
    auction_time = auction.start_date
    if (auction.start_date < datetime.now()):
        loadview(data)
        auction_done(data)
    else:
        emit("auction_status", {"status": "running","remained":remained,"server_time":str(server_time),"auction_time":str(auction_time)},room=room)

@socketio.on('get_remain_time')
def get_remain_time(data):
    room = data['auction_id']
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    if(auction.start_date < datetime.now()):
        auction_done(data)
    else:
        remained = (auction.start_date - datetime.now()).seconds + 1
        emit("remaining_time", remained,room=room)

@socketio.on('keepAlive')
def keepAlive(data):
    room = data['auction_id']
    emit("alive",room=room)
