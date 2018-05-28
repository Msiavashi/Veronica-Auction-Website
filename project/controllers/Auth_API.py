# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask_restful import Resource, reqparse
from project.model.user import *
from flask_jwt_extended import (create_access_token,create_refresh_token,set_access_cookies,set_refresh_cookies)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
from ..model import Order, Item, Payment
import json
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

parser_register = reqparse.RequestParser()
parser_register.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_register.add_argument('mobile', help = 'ورود شماره همراه ضروری است', required = True)
parser_register.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_register.add_argument('c_password', help = 'ورود تکرار رمز عبور ضروری است', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_login.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)

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
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return make_response(jsonify({'success': True,'access_token': access_token,'refresh_token': refresh_token}),200)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)
    def get(self):
        return make_response(jsonify({"message":"online resources register"}),404)

class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args()

        current_user = User.find_by_username(data['username'])

        if not current_user:
            return make_response(jsonify({"message" :{"error" :'کاربری با نام کاربری مورد نظر شما پیدا نشد'}}),400)

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            login_user(current_user,remember=True)
            next = request.args.get('next')
            # Set the JWT cookies in the response
            resp = jsonify({
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'next':next})


            #create order
            if "items" in session:
                new_order = Order()
                new_order.user_id = current_user.id
                items = [Item.query.get(item_id) for item_id in session['items']]
                new_order.items = items
                new_order.total_cost += sum([item.price for item in items])
                db.session.add(new_order)
                db.session.commit()

            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return make_response(resp,200)
        else:
            return make_response(jsonify({'message':{"error" : 'رمز عبور شما نادرست است'}}),401)

    def get(self):
        return make_response(jsonify({"message":"online resources login"}),404)

# class Logout(object):
#     def post(self):
#         resp = jsonify({'logout': True})
#         unset_jwt_cookies(resp)
#         return resp, 200

# class UserLogout(Resource):
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return make_response(jsonify({'message': 'Access token has been revoked'}),200)
#         except Exception as e:
#             return make_response(jsonify({'message':{ 'error' : str(e)}}), 500)
#

# class UserLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Refresh token has been revoked'}
#         except:
#             return {'message': 'Something went wrong'}, 500
#
# class TokenRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity = current_user)
#         resp = jsonify({'refrech':True})
#         set_access_cookies(resp, access_token)
#         return resp,200
