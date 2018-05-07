# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
app.debug = True
toolbar = DebugToolbarExtension(app)
csrf = CSRFProtect(app)

from project.route import route
from project.controllers import *
from flask_restful import Api

api = Api(app,'/api')
api.add_resource(Auth_API.UserRegistration,'/register')
api.add_resource(Auth_API.UserLogin, '/login')
api.add_resource(Auth_API.UserLogout, '/logout')
api.add_resource(Auth_API.UserLogoutRefresh, '/logout/refresh')
api.add_resource(Auth_API.TokenRefresh, '/token/refresh')
api.add_resource(Site_API.CategoryMenuItems, '/category/menu/items')
api.add_resource(Site_API.AuctionCarouselAds, '/auction/carousel/ads')
api.add_resource(Site_API.ProductCarouselAds, '/product/carousel/ads')
api.add_resource(Site_API.SiteTodayEvents, '/today/events')
api.add_resource(Site_API.SiteTodayAuctions, '/today/auctions')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return project.model.RevokedTokenModel.is_jti_blacklisted(jti)
