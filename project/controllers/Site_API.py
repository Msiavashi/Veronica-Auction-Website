from flask_restful import Resource, reqparse
from ..model import *
from project.model.advertisement import *
from project.model.category import *
from project.model.event import *
from project.model.auction import *
from project.model.plan import *
from project.model.user_auction_like import user_auction_likes
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user


class CategoryMenuItems(Resource):
    def get(self):
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        return make_response(jsonify(category_schema.dump(categories)),200)

class AuctionCarouselAds(Resource):
    def get(self):
        advertisements = Advertisement.query.join(Auction).filter(Advertisement.show==True)
        ads_schema = AdvertisementSchema(many=True)
        return make_response(jsonify(ads_schema.dump(advertisements)),200)

class ProductCarouselAds(Resource):
    def get(self):
        advertisements = Advertisement.query.join(Product).filter(Advertisement.show==True)
        ads_schema = AdvertisementSchema(many=True)
        return make_response(jsonify(ads_schema.dump(advertisements)),200)

class SiteTodayEvents(Resource):
    def get(self):
        today = datetime.today()
        events = Event.query.filter_by(active = True).filter(Event.start_date <= today).filter(Event.end_date >= today).all()
        event_schema = EventSchema(many=True)
        return make_response(jsonify(event_schema.dump(events)),200)

class SiteTodayAuctions(Resource):
    def get(self):
        today = datetime.today()
        auctions = Auction.query.filter(Auction.start_date <= today ,Auction.end_date >= today).all()
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostpopularAuctions(Resource):
    def get(self):
        today = datetime.today()
        result = db.session.query(Auction.id, db.func.count(user_auction_likes.c.user_id).label('total')).join(user_auction_likes).group_by(Auction.id).having(Auction.end_date >= today).order_by('total DESC')
        auctions =[]
        for auction in result:
            auctions.append(Auction.query.get(auction.id))
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostpopularProducts(Resource):
    def get(self):
        today = datetime.today()
        result = db.session.query(Auction.id, db.func.count(user_product_likes.c.user_id).label('total')).join(Item).join(Product).join(user_product_likes).group_by(Auction.id).having(Auction.end_date >= today).order_by('total DESC')
        auctions =[]
        for auction in result:
            auctions.append(Auction.query.get(auction.id))
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction_schema = AuctionSchema()
        return make_response(jsonify(auction_schema.dump(auction)),200)

class AuctionPlans(Resource):
    def get(self):
        plans = Plan.query.all()
        plan_schema = PlanSchema(many=True)
        return make_response(jsonify(plan_schema.dump(plans)),200)

class UserParticipateAuction(Resource):
    def post(self):
        try:
            plan = Plan.query.get(request.form.get('plan_id'))
            auction = Auction.query.get(request.form.get('auction_id'))
            current_user.plans.append(plan)
            current_user.auctions.append(auction)
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({'success':True}),200)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)
