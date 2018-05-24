# -*- coding: utf-8 -*-
import sys
from importlib import reload
reload(sys)
# sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
import time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from decimal import Decimal

class AuctionUserViewed(Resource):
    def get(self):
        auctions = Auction.query.join(user_auction_views).filter_by(user_id=current_user.id)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class AuctionUserParticipation(Resource):
    def post(self):
        plan_id = request.form.get('plan_id')
        auction_id = request.form.get('auction_id')
        payment_method_id = request.form.get('method_id')
        amount = request.form.get('amount')

        auction = Auction.query.get(auction_id)

        now = datetime.now()
        remained = (auction.start_date - now).seconds
        if(remained < 60):
            return make_response(jsonify({'success':False,"reason":"حداکثر تا یک دقیقه قبل از حراجی برای ثبت نام فرصت دارید"}),400)

        plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()
        auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction.id).first()
        user_plan = UserPlan()
        user_plan.auction = auction
        user_plan.auction_plan = auction_plan
        current_user.auctions.append(auction)
        current_user.user_plans.append(user_plan)

        current_user.credit -= Decimal(amount)

        db.session.add(current_user)
        db.session.commit()

        return make_response(jsonify({'success':True,"reason":"شرکت در حراجی با موفقیت انجام شد"}),200)
class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction.participants.order_by('created_at')
        auction_schema = AuctionSchema()
        product = Product.query.join(Item).join(Auction).filter_by(item_id=auction.item_id,id=auction.id).first()
        product_schema = ProductSchema()
        auction.remained_time = (auction.start_date - datetime.now()).seconds * 1000

        print '****************'+ str(datetime.now())+'******************'

        now_milliseconds = int(round(time.time() * 1000))
        now_date = datetime.now()


        if(current_user.is_authenticated):
            plan = AuctionPlan.query.join(UserPlan).filter_by(user_id=current_user.id,auction_id=aid).first()
            auction_plan_schema = AuctionPlanSchema()
            return make_response(jsonify({"server_now_date":now_date,"server_time_mili":now_milliseconds,"auction" : auction_schema.dump(auction) , "product" : product_schema.dump(product),"plan": auction_plan_schema.dump(plan)}),200)

        return make_response(jsonify({"server_now_date":now_date,"server_time_mili":now_milliseconds,"auction" : auction_schema.dump(auction) , "product" : product_schema.dump(product),"plan":[]}),200)
class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        payment_methods = PaymentMethod.query.all()
        payment_method_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify({"plans":plan_schema.dump(plans),"methods":payment_method_schema.dump(payment_methods)}),200)
