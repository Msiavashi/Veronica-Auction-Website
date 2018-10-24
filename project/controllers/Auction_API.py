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

class AuctionTestJson(Resource):
    def post(self):
        data = request.get_json(force=True)
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
                "id":user.id
            })

        user_schema = UserSchema(many=True)
        return make_response(jsonify({"success":True, "current_offer_price": str(last_offer.total_price),"users": users}),200)

class AuctionTest(Resource):
    def post(self):
        data = request.get_json(force=True)
        auction_id = data['auction_id']
        # auction = Auction.query.get(auction_id)
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price
            users.append(user)

        user_schema = UserSchema(many=True)

        return make_response(jsonify({"success":True, "current_offer_price": str(last_offer.total_price),"users": user_schema.dump(users)}),200)


class AuctionUserViewed(Resource):
    def get(self):
        if(current_user.is_authenticated):
            result = Auction.query.join(user_auction_views).filter_by(user_id=current_user.id).order_by('user_auction_views.date DESC').limit(10)
            auctions = []
            for auction in result:
                auction_participants = []
                for participant in auction.participants:
                    auction_participants.append({"id":participant.id,"username":participant.username})
                title = auction.title
                if (len(auction.title) > 15):
                    title = auction.title[:15]+"..."
                auctions.append({
                "id":auction.id,
                "title":title,
                "images":auction.item.images,
                "base_price":str(auction.base_price),
                "participants":auction_participants,
                })
            return make_response(jsonify(auctions),200)

class AuctionViewFinished(Resource):
    def get(self):
        result = Offer.query.filter_by(win=True).all()
        offers = []
        for offer in result:
            user = User.query.join(UserPlan).join(Offer).filter_by(id=offer.id).first()
            auction_participants = []
            for participant in offer.auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            winner = ""
            if(user.first_name and user.last_name and offer.win):
                winner = user.first_name + ' ' + user.last_name
            else:
                winner = user.username

            offers.append({
            "auction_id":offer.auction.id,
            "title":offer.auction.title,
            "images":offer.auction.item.images,
            "total_price":int(offer.total_price),
            "main_price":int(offer.auction.item.price),
            "start_date":offer.auction.start_date,
            "participants":auction_participants,
            "winner":winner,
            })
        return make_response(jsonify(offers),200)

class AuctionUserParticipation(Resource):
    def post(self):
        data = request.get_json(force=True)
        plan_id = int(data.get("plan_id", None))
        auction_id = int(data.get("auction_id", None))
        method_id = int(data.get("method_id", None))

        plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()
        auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction_id).first()
        payment_method = PaymentMethod.query.get(method_id)

        if not payment_method or not plan or not auction_plan:
            return make_response(jsonify({'success':False,"reason":"پلنی برای این حراجی تعریف نشده است"}),400)

        auction = auction_plan.auction
        now = datetime.now()
        remained = (auction.start_date - now).seconds

        if(auction.start_date < now):
            return make_response(jsonify({'success':False,"reason":"زمان شرکت در حراجی منقضی شده است"}),400)

        if(remained < 60):
            return make_response(jsonify({'success':False,"reason":"حداکثر تا یک دقیقه قبل از حراجی برای ثبت نام فرصت دارید"}),400)

        UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id,auction_id=auction.id).delete()
        amount = auction_plan.price

        if(payment_method.type == Payment_Types.Credit):
            if amount == 0 :
                payment = Payment()
                payment.type = PaymentType.FREE
                payment.ref_id = random.randint(10000,100000)
                payment.sale_order_id = random.randint(10000,100000)
                payment.sale_refrence_id = random.randint(10000,100000)
                payment.amount = amount
                payment.discount = 0
                payment.payment_method = payment_method
                payment.status = PaymentStatus.PAID

                user_plan = UserPlan()
                user_plan.auction = auction
                user_plan.auction_plan = auction_plan
                user_plan.payment = payment

                current_user.payments.append(payment)
                current_user.auctions.append(auction)
                current_user.user_plans.append(user_plan)

                db.session.add(current_user)
                db.session.commit()
                msg = "شما بصورت رایگان در این حراجی شرکت داده شدید"
                return make_response(jsonify({"success":True,"type":"registered","message":msg}),200)

            if(current_user.credit < amount):
                msg = "موجودی حساب شما برای پرداخت این پلن کافی نمی باشد"
                return make_response(jsonify({'success':False,"reason":msg}),400)

            payment = Payment()
            payment.type = PaymentType.PLAN
            payment.ref_id = current_user.id
            payment.sale_order_id = current_user.id
            payment.sale_refrence_id = current_user.id
            payment.amount = amount
            payment.discount = 0
            payment.payment_method = payment_method
            payment.status = PaymentStatus.PAID

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
            payment.type = PaymentType.PLAN
            payment.payment_method = payment_method
            payment.status = PaymentStatus.UNPAID
            payment.discount = 0

            user_plan = UserPlan()
            user_plan.auction = auction
            user_plan.auction_plan = auction_plan
            user_plan.payment = payment

            db.session.add(user_plan)
            db.session.commit()

            current_user.payments.append(payment)
            current_user.user_plans.append(user_plan)

            db.session.add(current_user)
            db.session.commit()

            msg = " برای پرداخت به صفحه تایید هدایت می شوید"
            return make_response(jsonify({'success':True,"type":"redirect_to_bank","pid":payment.id,"message":msg}),200)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction_participants = []
        for participant in auction.participants.order_by('created_at'):
            auction_participants.append({"id":participant.id,"username":participant.username})

        now = datetime.now()
        days = (auction.start_date - now).days
        sign = lambda x: (1, -1)[x < 0]
        remained_time = sign(days) *  (auction.start_date - now).seconds

        plan = None
        if(current_user.is_authenticated):
            plan = AuctionPlan.query.join(UserPlan).filter_by(user_id=current_user.id,auction_id=aid).first()
        result = None
        if plan:
            result = {
            "id":auction.id,
            "item_id":auction.item.id,
            "title":auction.title,
            "ratio":auction.ratio,
            "description":auction.description,
            "product_description":auction.item.product.description,
            "images":auction.item.images,
            "max_members":auction.max_members,
            "base_price":int(auction.base_price),
            "max_price":int(auction.max_price),
            "main_price":int(auction.item.price),
            "start_date":auction.start_date,
            "participants":auction_participants,
            "remained_time":remained_time,
            "max_offers":plan.max_offers
            }
        else:
            result = {
            "id":auction.id,
            "item_id":auction.item.id,
            "title":auction.title,
            "ratio":auction.ratio,
            "description":auction.description,
            "product_description":auction.item.product.description,
            "images":auction.item.images,
            "max_members":auction.max_members,
            "max_price":str(auction.max_price),
            "base_price":str(auction.base_price),
            "main_price":str(auction.item.price),
            "start_date":auction.start_date,
            "participants":auction_participants,
            "remained_time":remained_time,
            "max_offers":0
            }
        return make_response(jsonify({"auction":result}),200)

class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        payment_methods = PaymentMethod.query.order_by('type')
        payment_method_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify({"plans":plan_schema.dump(plans),"methods":payment_method_schema.dump(payment_methods)}),200)
