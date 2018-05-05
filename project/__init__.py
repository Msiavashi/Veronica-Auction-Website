# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
app.debug = True
toolbar = DebugToolbarExtension(app)
csrf = CSRFProtect(app)

from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user

login_manager = LoginManager()
login_manager.init_app(app)


from project.route import route
from project.controllers import *
from flask_restful import Api
import project.resources

api = Api(app,'/api')

api.add_resource(resources.UserRegistration,'/register')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogout, '/logout')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return project.model.RevokedTokenModel.is_jti_blacklisted(jti)
