from flask_restful import Resource, reqparse
from project.model import *
from project.model.advertisement import *
from project.model.category import *
from project.model.event import *
from project.model.auction import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime

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
        auctions = Auction.query.filter(Auction.start_date <= today).filter(Auction.end_date >= today).all()
        for auction in auctions:
            date_obj = auction.end_date.strftime('%Y-%m-%d %H:%M:%S')
            auction.remained =str(date_obj)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostpopularAuctions(Resource):
    def get(self):
        select = 'SELECT auctions.*,count(auctions.id) as total FROM auctions inner join user_auction_likes on auctions.id = user_auction_likes.auction_id group by auctions.id order by total DESC'
        auctions=Auction.query.from_statement(select)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostpopularProducts(Resource):
    def get(self):
        select = 'SELECT auctions.*,count(*)as total FROM auctions inner join items on items.id=auctions.item_id inner join products on products.id=items.product_id inner join user_product_likes on user_product_likes.product_id=products.id group by(auctions.id) order by total DESC'
        auctions=Auction.query.from_statement(select)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction_schema = AuctionSchema()
        return make_response(jsonify(auction_schema.dump(auction)),200)
