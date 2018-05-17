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
        try:
            plan_id = request.form.get('plan_id')
            auction_id = request.form.get('auction_id')
            print auction_id,plan_id
            print "***************"

            auction = Auction.query.get(auction_id)
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
                return make_response(jsonify({'success':True}),200)
            else:
                return make_response(jsonify({'success':False}),400)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction_schema = AuctionSchema()
        return make_response(jsonify(auction_schema.dump(auction)),200)

class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        return make_response(jsonify(plan_schema.dump(plans)),200)
