#*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from project.model.user import *
from flask_jwt_extended import (set_refresh_cookies,create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,set_access_cookies)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
from ..model import *
from ..model.order import *
import json
from ..database import db
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

parser_register = reqparse.RequestParser()
parser_register.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_register.add_argument('mobile', help = 'ورود شماره همراه ضروری است', required = True)
parser_register.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_register.add_argument('c_password', help = 'ورود تکرار رمز عبور ضروری است', required = True)
parser_register.add_argument('accept_roles', help = 'تایید مقررات سایت الزامی است', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_login.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_login.add_argument('remember_me', required = False)
parser_login.add_argument('next')

def can_access(f):
    if not hasattr(f, 'access_control'):
        return True
    return _eval_access(**f.access_control) == AccessResult.ALLOWED

class UserRegistration(Resource):
    def post(self):
        data = parser_register.parse_args()

        if User.find_by_username(data['username']):
            return make_response(jsonify({"message":{"username":'کاربری با این مشخصات از قبل تعریف شده است'}}),400)

        if(data['password']!=data['c_password']):
            return make_response(jsonify({"message":{'password': 'رمز عبور با تکرار آن مطابقت ندارد'}}),400)

        new_user = User(data['username'])
        new_user.username = data['username']
        new_user.mobile = data['mobile']
        new_user.password = User.generate_hash(data['password'])

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'],fresh=True,expires_delta=False)
            refresh_token = create_refresh_token(identity = data['username'])
            return make_response(jsonify({'success': True,'access_token': access_token,'refresh_token': refresh_token}),200)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)
    def get(self):
        return make_response(jsonify({"message":"online resources register"}),404)


class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args()
        data = request.get_json(force=True)

        current_user = User.find_by_username(data['username'])

        if not current_user:
            return make_response(jsonify({"message" :{"error" :'کاربری با نام کاربری مورد نظر شما پیدا نشد'}}),400)

        if User.verify_hash(data['password'], current_user.password):


            access_token = create_access_token(identity = data['username'],fresh=True,expires_delta=False)
            refresh_token = create_refresh_token(identity = data['username'])

            # Set the JWT cookies in the response
            redirect_to_auction = False
            auction_id = 0

            if 'next' in data and "participate" in data['next'] :
                temp = data['next']
                auction_id = temp.split('/')[2]
                if(current_user.has_auction(int(auction_id))):
                    redirect_to_auction = True

            if redirect_to_auction:
                resp = jsonify({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'redirect_to_auction': redirect_to_auction,
                    'auction_id':auction_id
                    })
            else:
                resp = jsonify({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    })

            # create orders from session on login
            if "orders" in session:
                order_schema = OrderSchema(many=True)
                for order in session['orders']:
                    new_order = Order()
                    item = Item.query.get(order[0]['item']['id'])
                    saved_before = Order.query.filter_by(user_id=current_user.id).join(Item).filter_by(id=item.id).first()
                    if not saved_before:
                        #calculate price base on auction participation
                        total = int(order[0]['total'])
                        item_price = (item.price - item.discount) * total
                        discount_status = OrderDiscountStatus.REGULAR
                        discount = item.discount * total

                        auction = current_user.auctions.join(Item).filter_by(id = item.id).first()
                        if auction:
                            offer = Offer.query.join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                            discount_status = OrderDiscountStatus.INAUCTION
                            if offer and offer.win:
                                item_price = offer.total_price
                                discount_status = OrderDiscountStatus.AUCTIONWINNER
                                total = 1
                                discount = item.price - offer.total_price
                            else:
                                userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                                auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                                item_price = item.price - auctionplan.discount
                                total = 1
                                discount = auctionplan.discount

                        new_order.item = item
                        new_order.total_cost = item_price
                        new_order.total = total
                        new_order.status = OrderStatus.UNPAID
                        new_order.discount_status = discount_status
                        new_order.total_discount = discount
                        new_order.user = current_user;
                        db.session.add(new_order)
                        db.session.commit()
                session.pop('orders')

            if 'remember_me' in data and data['remember_me']==True:
                login_user(current_user,remember=True)
            else:
                login_user(current_user,remember=False)

            set_refresh_cookies(resp, refresh_token)
            set_access_cookies(resp, access_token)
            return make_response(resp,200)
        else:
            return make_response(jsonify({'message':{"error" : 'رمز عبور شما نادرست است'}}),401)

    def get(self):
        return make_response(jsonify({"message":"online resources login"}),404)

class Logout(object):
    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return make_response(resp,200)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return make_response(jsonify({'message': 'Access token has been revoked'}),200)
        except Exception as e:
            return make_response(jsonify({'message':{ 'error' : str(e)}}), 500)


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        resp = jsonify({'access_token': access_token})
        resp = jsonify({
            'message': 'Token refreshed for {}'.format(current_user),
            'access_token': access_token,
            })
        set_access_cookies(resp, access_token)
        return make_response(resp,200)
