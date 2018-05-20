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
from datetime import datetime
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

def offer_bid(data):
    try:
        # if(not current_user.is_authenticated):
        #     return '{"success":"false","reason":"لطفا قبل از ارسال پیشنهاد به سایت وارد شوید"}'
        #
        auction_id = data['auction_id']
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('created_at DESC').first()
        if(last_offer and last_offer.win):
            winner = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(id=last_offer.id).first()
            user_schema = UserSchema()
            return '{"success":"true","handler":"auction_done","winner":'+json.dumps(user_schema.dump(winner))+'}'

        user_id = data['user_id']
        auction = Auction.query.get(auction_id)

        today = datetime.today()
        if(auction.start_date < today):
            return '{"success":"false","reason":"مهلت ارسال پیشنهادات به اتمام رسیده است"}'


        user = User.query.get(user_id)
        user_plan = UserPlan.query.filter_by(user_id=user_id,auction_id=auction_id).first()
        my_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('created_at DESC').first()
        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1

        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer):
            if(my_last_offer.current_bids > 0):
                offer.total_price = auction.base_price + offer_count * (BASE_BID_PRICE * auction.ratio)
                offer.current_bids = my_last_offer.current_bids - 1
            else:
                return '{"success":"false","reason":"پیشنهادات شما به پایان رسید"}'
        else:
            offer.total_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1

        db.session.add(offer)
        db.session.commit()

        all_bids = Offer.query.filter_by(auction_id=auction.id).count()
        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        user_schema = UserSchema(many=True)
        return '{"handler":"offer","success":"true","total_price":'+str(offer.total_price)+',"users":'+json.dumps(user_schema.dump(users))+',"total_bids":'+str(all_bids)+'}'


        # user_plan = UserPlan.query.filter_by(user_id=user_id,auction_id=auction_id).first()
        # auction_plan = AuctionPlan.query.get(user_plan.auction_plan_id)
        #
        # offer = Offer()
        # offer.user_plan = user_plan
        # offer.auction = auction
        # offer.current_bids = UserPlan.query.filter_by(user_id=user.id,auction_id=auction.id).count()
        # offer.total_price =  BASE_BID_PRICE * auction.ratio
        # print "here i am***************"
        # db.session.add(offer)
        # db.session.commit()
        return "{'success':'true','auction':"+auction.name+",'user':"+user.username+"'offers:'"+offers+"}"
    except Exception as e:
        return "{'error':"+str(e)+"}"

def loadview(data):
    try:
        auction_id = data['auction_id']
        total_bids = Offer.query.filter_by(auction_id=auction_id).count()
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('created_at DESC').first()
        users = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('total_price DESC')
        user_schema = UserSchema(many=True)
        if(last_offer):
            return '{"success":"true","handler":"loadview","total_bids": "'+ str(total_bids) +'","current_offer_price":"'+ str(last_offer.total_price) +'" ,"users":'+json.dumps(user_schema.dump(users))+'}'
        else:
            return '{"success":"true","handler":"loadview","total_bids": "0","current_offer_price":"0" ,"users":'+json.dumps(user_schema.dump(users))+'}'

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
            return '{"success":"true","handler":"auction_done","winner":'+json.dumps(user_schema.dump(winner))+'}'
        else:
            return '{"success":"false","handler":"auction_done" , "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"}'
    except Exception as e:
        return "{'error':"+str(e)+"}"
