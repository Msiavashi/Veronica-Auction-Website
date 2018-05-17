from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user


class SiteCategoryMenuItems(Resource):
    def get(self):
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        return make_response(jsonify(category_schema.dump(categories)),200)

class SiteCategoryAuctions(Resource):
    def get(self,cid):
        auctions = Auction.query.join(Item).join(Product).join(Category).filter_by(id = cid)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteAuctionCarouselAds(Resource):
    def get(self):
        auctions = Auction.query.join(Advertisement).filter(Advertisement.show==True)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteProductCarouselAds(Resource):
    def get(self):
        products = Product.query.join(Advertisement).filter(Advertisement.show==True)
        product_schema = ProductSchema(many=True)
        return make_response(jsonify(product_schema.dump(products)),200)

class SiteTodayEvents(Resource):
    def get(self):
        today = datetime.today()
        events = Event.query.filter_by(is_active = True).filter(Event.start_date <= today).filter(Event.end_date >= today).all()
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

class SiteMostviewedAuctions(Resource):
    def get(self):
        today = datetime.today()
        result = db.session.query(Auction.id, db.func.count(user_auction_views.c.user_id).label('total')).join(user_auction_views).group_by(Auction.id).having(Auction.end_date >= today).order_by('total DESC')
        auctions =[]
        for auction in result:
            auctions.append(Auction.query.get(auction.id))
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

# class SiteMostpopularProducts(Resource):
#     def get(self):
#         today = datetime.today()
#         result = db.session.query(Auction.id, db.func.count(user_product_likes.c.user_id).label('total')).join(Item).join(Product).join(user_product_likes).group_by(Auction.id).having(Auction.end_date >= today).order_by('total DESC')
#         auctions =[]
#         for auction in result:
#             auctions.append(Auction.query.get(auction.id))
#         auction_schema = AuctionSchema(many=True)
#         return make_response(jsonify(auction_schema.dump(auctions)),200)
