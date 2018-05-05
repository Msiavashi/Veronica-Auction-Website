# # encoding=utf8
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from flask_restful import Resource, reqparse
from project.model.user import User
from project.model.revoke import RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


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

        new_user = User(
            username = data['username'],
            mobile = data['mobile'],
            password = User.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return jsonify({'success': True,'access_token': access_token,'refresh_token': refresh_token}),200
        except Exception as e:
            return jsonify({'messages': str(e)}), 500



class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args()

        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            login_user(current_user)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}

    def get(self):
        return render_template('site/login.html')

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            return {'message':str(e)}, 500


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


class AllUsers(Resource):
    def get(self):
        return

    def delete(self):
        return {'message': 'Delete all users'}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
