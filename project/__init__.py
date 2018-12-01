# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__version__ = '0.1'
from functools import wraps
from flask import Flask , session , Response , render_template ,request ,g
from flask_restful import reqparse, abort, Api, Resource
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
# from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()
import redis
from flask_login import current_user,LoginManager
from definitions import SESSION_EXPIRE_TIME,SMS_USERNAME,SMS_PASSWORD
from flask_session import Session
from sqlalchemy import create_engine
import melipayamak
from flask_mail import Mail

REDIS_URL = "redis://localhost:6379/0"


app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)

jwt = JWTManager(app)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return model.Revoked.is_jti_blacklisted(jti)

# after production comment this
# Session(app)

params = {
	 'pingInterval': 20000,
     'pingTimeout': 10000,
}
#
# socketio = SocketIO(logger=True, engineio_logger=True, **params)

socketio = SocketIO(**params)
socketio.init_app(app, message_queue=REDIS_URL,async_mode='eventlet',manage_session=False)

app.debug = False
toolbar = DebugToolbarExtension(app)

#login manager

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'site.login'

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.permanent_lifetime = timedelta(days=SESSION_EXPIRE_TIME)


#
# @app.after_request
# def after_request(response):
#     if g.db is not None:
#         g.db.close()
#     return response

def verify_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.is_verified:
                return render_template('site/verify.html'), 400
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper

def iverify_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.is_verified:
                return render_template('site/iframes/verify.html'), 400
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper

from project.middleware import *
app.jinja_env.globals.update(has_role=has_role)

# csrf = CSRFProtect(app)

# sockets = Sockets(app)

# redis = redis.from_url(REDIS_URL)

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
# with app.app_context():
#         cache.clear()

# from websocket import broker
from .route import route
from .websocket import handler
from .controllers import *


@app.errorhandler(400)
def custom_401(error):
    return render_template('site/400.html'), 400
    # return Response('دسترسی شما به آدرس مورد نظر ممکن نیست', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})
# @app.after_request
# def apply_changing(response):
#     response.headers["X-Frame-Options"] = "Allow"
#     return response

# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400


# api = Api(app,'/api',decorators=[csrf.exempt])
api = Api(app,'/api')

api.add_resource(Auth_API.UserRegistration,'/register')
api.add_resource(Auth_API.UserVerification,'/user/verification')
api.add_resource(Auth_API.UserVerificationMail,'/user/verification/mail')
api.add_resource(Auth_API.UserLogin, '/user/login')
api.add_resource(Auth_API.UserLogout, '/user/logout')
api.add_resource(Auth_API.UserTokenRefresh, '/refresh/token')
api.add_resource(Auth_API.UserLogoutRefresh, '/refresh/logout')
api.add_resource(Auth_API.UserForgotPassword, '/user/forgot/password')
api.add_resource(Auth_API.UserChangePassword, '/user/change/password')

api.add_resource(Site_API.SiteCategoryMenuItems, '/site/category/menu/items')
api.add_resource(Site_API.SiteSearchAuctions, '/site/search/auctions/<keyword>')
api.add_resource(Site_API.SiteSearchAuctionsCategory, '/site/search/auctions/category/<int:cid>/<keyword>')
api.add_resource(Site_API.SiteSearchFilters, '/site/search/filters/<order_by_price>/<order_by>/<int:total>/<keyword>')

api.add_resource(Site_API.SiteCategoryAuctions, '/site/category/<int:cid>/auctions/')
api.add_resource(Site_API.SiteCategoryForAuctions, '/site/category/auctions/')
api.add_resource(Site_API.SiteCategoryProducts, '/site/category/<int:cid>/products/')
api.add_resource(Site_API.SiteCategoryProductFilters, '/site/category/<int:cid>/product/filters/<order_by_price>/<order_by>/<int:total>')
api.add_resource(Site_API.SiteCategoryCarouselAds, '/site/category/<int:cid>/carousel/ads')
api.add_resource(Site_API.SiteAuctionCarouselAds, '/site/auction/carousel/ads')
api.add_resource(Site_API.SiteProductCarouselAds, '/site/product/carousel/ads')
api.add_resource(Site_API.SiteTodayEvents, '/site/today/events')
api.add_resource(Site_API.SiteTodayAuctions, '/site/today/auctions')
api.add_resource(Site_API.SiteMostpopularAuctions, '/site/mostpopular/auctions')
api.add_resource(Site_API.SiteMostviewedAuctions, '/site/mostviewed/auctions')
api.add_resource(Site_API.SiteShipmentMethods, '/site/shipment/methods')
api.add_resource(Site_API.SitePaymentMethods, '/site/payment/methods')
api.add_resource(Site_API.SiteStates, '/site/address/states')

api.add_resource(Auction_API.AuctionInstanceView, '/auction/<int:aid>/instantview')
api.add_resource(Auction_API.AuctionGetPlans, '/auction/get/plans/<int:aid>')
api.add_resource(Auction_API.AuctionUserParticipation, '/auction/user/participation')
api.add_resource(Auction_API.AuctionUserViewed, '/auction/user/viewed')
api.add_resource(Auction_API.AuctionViewFinished, '/auction/view/finished')
api.add_resource(Auction_API.AuctionUsers, '/auction/users/<int:aid>')
api.add_resource(Auction_API.AuctionWinners, '/auction/winners/<int:aid>')

api.add_resource(User_API.PaymentsInfo, '/user/payments/info/<int:pagenum>/<int:pagesize>')
api.add_resource(User_API.UserInformation, '/user/information')
api.add_resource(User_API.UserBasicInfo, '/user/basic/information')
api.add_resource(User_API.UserContactUs, '/user/contactus')
api.add_resource(User_API.UserAuctionLikes, '/user/auction/likes')
api.add_resource(User_API.UserFavoriteFilters, '/user/favorite/filters/<order_by_price>/<order_by>/<int:total>')
api.add_resource(User_API.UserChargeWalet, '/user/charge/walet')
# api.add_resource(User_API.CartOrder, '/cart/order')
api.add_resource(Payment_API.MellatGateway, '/mellat/gateway')
api.add_resource(Payment_API.MellatGatewayCallBack, '/user/mellat/gateway/callback')

api.add_resource(Payment_API.ZarinpalGateway, '/zarinpal/gateway')
api.add_resource(Payment_API.ZarinpalGatewayCallback, '/user/zarinpal/gateway/callback')

api.add_resource(User_API.UserApplyPayment, '/user/apply/payment')
api.add_resource(User_API.UserCartOrder, '/user/cart/order')
api.add_resource(User_API.UserCartCheckout, '/user/cart/checkout')

api.add_resource(User_API.UserCheckoutConfirm, '/user/checkout/confirm/payment/<int:pid>')
api.add_resource(User_API.UserUnpaidOrders, '/user/orders/unpaid' )
api.add_resource(User_API.UserUnpaidPayments, '/user/payments/unpaids')
api.add_resource(User_API.UserAuctionView, '/user/auction/view')
api.add_resource(User_API.UserCoupons, '/user/coupons')
api.add_resource(User_API.UserCheckOutInit, '/user/checkout/payment/init')

api.add_resource(Auction_API.AuctionTestJson, '/auction/test/json')
api.add_resource(Auction_API.AuctionTest, '/auction/test')
