from flask_restful import Resource, reqparse
from project.model.user import *
from project.model.revoke import RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User(username)


parser_register = reqparse.RequestParser()
parser_register.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_register.add_argument('mobile', help = 'ورود شماره همراه ضروری است', required = True)
parser_register.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_register.add_argument('c_password', help = 'ورود تکرار رمز عبور ضروری است', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_login.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)


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
            return make_response(jsonify({
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }),200)
        else:
            return make_response(jsonify({'message':{"error" : 'رمز عبور شما نادرست است'}}),401)

    def get(self):
        return make_response(jsonify({"message":"online resources login"}),404)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return make_response(jsonify({'message': 'Access token has been revoked'}),200)
        except Exception as e:
            return make_response(jsonify({'message':{ 'error' : str(e)}}), 500)


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
