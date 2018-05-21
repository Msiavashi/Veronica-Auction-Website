# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user


class AuctionUserViewed(Resource):
    def get(self):
        auctions = Auction.query.join(user_auction_views).filter_by(user_id=current_user.id)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class AuctionUserParticipation(Resource):
    def post(self):
        plan_id = request.form.get('plan_id')
        auction_id = request.form.get('auction_id')
        auction = Auction.query.get(auction_id)
        now = datetime.now()
        remained = (auction.start_date - now).seconds
        
        if(remained < 60):
            return make_response(jsonify({'success':False,"reason":"حداکثر تا یک دقیقه قبل از حراجی برای ثبت نام فرصت دارید"}),400)

        plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()

        auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction.id).first()

        if(not current_user.has_auction(auction.id)):
            user_plan = UserPlan()
            user_plan.auction = auction;
            user_plan.auction_plan = auction_plan;
            current_user.auctions.append(auction)
            current_user.user_plans.append(user_plan)
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({'success':True,"reason":"شرکت در حراجی با موفقیت انجام شد"}),200)
        else:
            return make_response(jsonify({'success':False,"reason":"شما قبلا در این حراجی عضو شده اید"}),400)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction.participants.order_by('created_at')
        auction_schema = AuctionSchema()
        product = Product.query.join(Item).join(Auction).filter_by(item_id=auction.item_id,id=auction.id).first()
        product_schema = ProductSchema()
        return make_response(jsonify({"auction" : auction_schema.dump(auction) , "product" : product_schema.dump(product)}),200)

class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        return make_response(jsonify(plan_schema.dump(plans)),200)
