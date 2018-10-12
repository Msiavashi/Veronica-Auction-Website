# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
import os
from sqlalchemy import or_

from ..model.guest_message import GuestMessage
from definitions import MAX_SEARCH_RESULT


class SiteStates(Resource):
    def get(self):
        states = State.query.order_by('title').distinct().all()
        state_schema = StateSchema(many=True)
        return make_response(jsonify(state_schema.dump(states)),200)

class SiteSearchFilters(Resource):
    def get(self,order_by_price,order_by,total,keyword):
        now = datetime.now()
        result = None
        if order_by_price == "price":
            result = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).join(Item).order_by("price " + order_by).limit(total)
        else:
            result = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).order_by("start_date " + order_by).limit(total)

        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            auction.left_from_created = (auction.created_at - now).seconds
            if current_user.is_authenticated:
                auction.liked = auction in current_user.auction_likes
            auctions.append(auction)

        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteSearchAuctions(Resource):
    def get(self,keyword):
        auctions = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).limit(MAX_SEARCH_RESULT)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteSearchAuctionsCategory(Resource):
    def get(self,cid,keyword):
        auctions = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).join(Item).join(Product).join(Category).filter_by(id = cid)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteCategoryMenuItems(Resource):
    def get(self):
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        return make_response(jsonify(category_schema.dump(categories)),200)

class SiteCategoryAuctions(Resource):
    def get(self,cid):
        now = datetime.now()
        result = Auction.query.filter(Auction.start_date >= now).join(Item).join(Product).join(Category).filter_by(id = cid)
        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            auctions.append(auction)
        category = Category.query.get(cid)
        auction_schema = AuctionSchema(many=True)
        category_schema = CategorySchema()
        result ={'category':category_schema.dump(category),'auctions':auction_schema.dump(auctions)}
        return make_response(jsonify(result),200)

class SiteCategoryProducts(Resource):
    def get(self,cid):
        now = datetime.now()
        result = Auction.query.filter(Auction.start_date >= now).join(Item).order_by("price").join(Product).join(Category).filter_by(id = cid)
        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).seconds
            auction.left_from_created = (now.replace(hour=0,minute=0,second=0,microsecond=0) - now).seconds
            auctions.append(auction)
        category = Category.query.get(cid)
        auction_schema = AuctionSchema(many=True)
        category_schema = CategorySchema()
        result ={'category':category_schema.dump(category),'auctions':auction_schema.dump(auctions)}
        return make_response(jsonify(result),200)

class SiteCategoryProductFilters(Resource):
    def get(self,cid,order_by_price,order_by,total):
        now = datetime.now()
        result = None
        if order_by_price=="price":
            result = Auction.query.join(Item).order_by("price "+ order_by).join(Product).join(Category).filter_by(id = cid).limit(total)
        else:
            result = Auction.query.order_by("start_date "+ order_by).join(Item).join(Product).join(Category).filter_by(id = cid).limit(total)

        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            auction.left_from_created = (now.replace(hour=0,minute=0,second=0,microsecond=0) - now).seconds
            if current_user.is_authenticated:
                auction.liked = auction in current_user.auction_likes
            auctions.append(auction)
        category = Category.query.get(cid)
        auction_schema = AuctionSchema(many=True)
        category_schema = CategorySchema()
        result ={'category':category_schema.dump(category),'auctions':auction_schema.dump(auctions)}
        return make_response(jsonify(result),200)

class SiteAuctionCarouselAds(Resource):
    def get(self):
        auctions = Auction.query.join(Advertisement).filter(Advertisement.show==True)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteCategoryCarouselAds(Resource):
    def get(self,cid):
        now = datetime.now()
        auctions = Auction.query.filter(Auction.start_date >= now).join(Advertisement).filter(Advertisement.show==True).join(Item).join(Product).join(Category).filter_by(id = cid)
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
        events = Event.query.filter_by(is_active = True).filter(Event.start_date <= today , Event.end_date >= today).all()
        event_schema = EventSchema(many=True)
        return make_response(jsonify(event_schema.dump(events)),200)

class SiteTodayAuctions(Resource):
    def get(self):
        results = db.session.query(Auction).all()
        auctions=[]
        for auction in results:
            now = datetime.now()
            remained = (auction.start_date - now).days
            if(remained==0):
                auction.remained_time = (auction.start_date - now).seconds
                auctions.append(auction)

        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostpopularAuctions(Resource):
    def get(self):
        today = datetime.today()
        result = db.session.query(Auction.id, db.func.count(user_auction_likes.c.user_id).label('total')).join(user_auction_likes).group_by(Auction.id).having(Auction.start_date >= today).order_by('total DESC')
        auctions =[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - datetime.now()).seconds
            auctions.append(auction)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteMostviewedAuctions(Resource):
    def get(self):
        today = datetime.today()
        result = db.session.query(Auction.id, db.func.count(user_auction_views.c.user_id).label('total')).join(user_auction_views).group_by(Auction.id).having(Auction.start_date >= today).order_by('total DESC')
        auctions =[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - datetime.now()).seconds
            auctions.append(auction)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @login_required
    def post(self):

        new_message = GuestMessage()

        new_message.full_name = request.get.json('full_name', None)
        new_message.email = request.get.json('email', None)
        new_message.message = request.get.json('message', None)
        new_message.website = request.get.json('website', None)

        db.session.add(new_message)
        db.session.commit()

        flash("پیام با موفقیت ارسال شد")

        return redirect(url_for('index'))


class SitePaymentMethods(Resource):

    def get(self):
        payment_methods = PaymentMethod.query.order_by('type').all()
        payment_methods_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify(payment_methods_schema.dump(payment_methods)), 200)


class SiteShipmentMethods(Resource):

    def get(self):
        shipment_methods = ShipmentMethod.query.order_by('price').all()
        shipment_methods_schema = ShipmentMethodSchema(many=True)
        return make_response(jsonify(shipment_methods_schema.dump(shipment_methods)), 200)
