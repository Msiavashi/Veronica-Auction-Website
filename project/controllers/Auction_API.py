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
import time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import login_required ,current_user
from decimal import Decimal
import random

class AuctionUserViewed(Resource):
    def get(self):
        if(current_user.is_authenticated):
            auctions = Auction.query.join(user_auction_views).filter_by(user_id=current_user.id)
            auction_schema = AuctionSchema(many=True)
            return make_response(jsonify(auction_schema.dump(auctions)),200)

class AuctionViewFinished(Resource):
    def get(self):
        offers = Offer.query.filter_by(win=True).all()
        for offer in offers:
            user = User.query.join(UserPlan).join(Offer).filter_by(id=offer.id).first()
            user_schema = UserSchema()

            if(user.first_name and user.last_name and offer.win):
                offer.winner = user.first_name + ' ' + user.last_name
            else:
                offer.winner = user.username

        offer_schema = OfferSchema(many=True)
        return make_response(jsonify(offer_schema.dump(offers)),200)

class AuctionUserParticipation(Resource):
    def post(self):
        plan_id = request.form.get('plan_id')
        auction_id = request.form.get('auction_id')
        payment_method_id = request.form.get('method_id')
        payment_method = PaymentMethod.query.get(payment_method_id)

        amount = request.form.get('amount')
        if not amount:
            return make_response(jsonify({'success':False,"reason":"پلنی برای این حراجی تعریف نشده است"}),400)


        auction = Auction.query.get(auction_id)

        now = datetime.now()
        remained = (auction.start_date - now).seconds

        if(remained < 60):
            return make_response(jsonify({'success':False,"reason":"حداکثر تا یک دقیقه قبل از حراجی برای ثبت نام فرصت دارید"}),400)

        if(payment_method.type == Payment_Types.Credit):
            if(current_user.credit < int(amount)):
                msg = "موجودی حساب شما برای پرداخت این پلن کافی نمی باشد"
                return make_response(jsonify({'success':False,"reason":msg}),400)

            payment = Payment()
            payment.ref_id = current_user.id
            payment.sale_order_id = current_user.id
            payment.sale_refrence_id = current_user.id
            payment.GUID = random.randint(100000,100000000)
            payment.amount = amount
            payment.payment_method = payment_method
            payment.status = PaymentStatus.PAID

            plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()
            auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction.id).first()
            unpain_user_plan = UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id,auction_id=auction.id).delete()

            user_plan = UserPlan()
            user_plan.auction = auction
            user_plan.auction_plan = auction_plan
            user_plan.payment = payment

            current_user.payments.append(payment)
            current_user.auctions.append(auction)
            current_user.user_plans.append(user_plan)
            current_user.credit -= Decimal(amount)

            db.session.add(current_user)
            db.session.commit()
            msg = "شرکت در حراجی با موفقیت انجام شد"
            return make_response(jsonify({"success":True,"type":"registered","message":msg}),200)

        if(payment_method.type == Payment_Types.Online):

            payment = Payment()
            payment.amount = amount
            payment.payment_method = payment_method
            payment.status = PaymentStatus.UNPAID

            plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()
            auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction.id).first()
            unpain_user_plan = UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id,auction_id=auction.id).delete()
            db.session.commit()


            user_plan = UserPlan()
            user_plan.auction = auction
            user_plan.auction_plan = auction_plan
            user_plan.payment = payment

            db.session.add(user_plan)
            db.session.commit()

            current_user.payments.append(payment)
            # current_user.auctions.append(auction)
            current_user.user_plans.append(user_plan)

            db.session.add(current_user)
            db.session.commit()

            msg = " برای پرداخت به صفحه تایید هدایت می شوید"
            return make_response(jsonify({'success':True,"type":"redirect_to_bank","pid":payment.id,"message":msg}),200)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction.participants.order_by('created_at')
        auction_schema = AuctionSchema()
        product = Product.query.join(Item).join(Auction).filter_by(item_id=auction.item_id,id=auction.id).first()
        product_schema = ProductSchema()
        auction.remained_time = (auction.start_date - datetime.now()).seconds

        if(current_user.is_authenticated):
            plan = AuctionPlan.query.join(UserPlan).filter_by(user_id=current_user.id,auction_id=aid).first()
            auction_plan_schema = AuctionPlanSchema()
            return make_response(jsonify({"auction" : auction_schema.dump(auction) , "product" : product_schema.dump(product),"plan": auction_plan_schema.dump(plan)}),200)
        return make_response(jsonify({"auction" : auction_schema.dump(auction) , "product" : product_schema.dump(product),"plan":[]}),200)

class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        payment_methods = PaymentMethod.query.all()
        payment_method_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify({"plans":plan_schema.dump(plans),"methods":payment_method_schema.dump(payment_methods)}),200)
