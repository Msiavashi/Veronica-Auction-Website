# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__version__ = '0.1'
from flask import Flask , session
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
# from flask_caching import Cache
from flask_sockets import Sockets
import redis


REDIS_URL = "redis://localhost:6379/0"

app = Flask(__name__)
app.config.from_pyfile('config.py')
jwt = JWTManager(app)
app.debug = True
toolbar = DebugToolbarExtension(app)
# csrf = CSRFProtect(app)

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
# with app.app_context():
#         cache.clear()

from websocket import broker
from .route import route
from .controllers import *
from flask_restful import Api

api = Api(app,'/api')

api.add_resource(Auth_API.UserRegistration,'/register')
api.add_resource(Auth_API.UserLogin, '/login')
# api.add_resource(Auth_API.UserLogout, '/logout')

api.add_resource(Site_API.SiteCategoryMenuItems, '/site/category/menu/items')
api.add_resource(Site_API.SiteCategoryAuctions, '/site/category/<int:cid>/auctions/')
api.add_resource(Site_API.SiteAuctionCarouselAds, '/site/auction/carousel/ads')
api.add_resource(Site_API.SiteProductCarouselAds, '/site/product/carousel/ads')
api.add_resource(Site_API.SiteTodayEvents, '/site/today/events')
api.add_resource(Site_API.SiteTodayAuctions, '/site/today/auctions')
api.add_resource(Site_API.SiteMostpopularAuctions, '/site/mostpopular/auctions')
api.add_resource(Site_API.SiteMostviewedAuctions, '/site/mostviewed/auctions')

api.add_resource(Auction_API.AuctionInstanceView, '/auction/<int:aid>/instantview')
api.add_resource(Auction_API.AuctionGetPlans, '/auction/get/plans/<int:aid>')
api.add_resource(Auction_API.AuctionUserParticipation, '/auction/user/participation')
api.add_resource(Auction_API.AuctionUserViewed, '/auction/user/viewed')


api.add_resource(User_API.DashBoard, '/user/profile/info')
api.add_resource(User_API.PaymentsInfo, '/user/payments/info')