# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

__version__ = '0.1'
from flask import Flask , session , Response , render_template
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
# from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_socketio import SocketIO
import websocket
import eventlet
eventlet.monkey_patch(socket=True)
import redis
from flask_login import current_user,LoginManager
from definitions import SESSION_EXPIRE_TIME

REDIS_URL = "redis://localhost:6379/0"

app = Flask(__name__)
app.config.from_pyfile('config.py')
socketio = SocketIO()
socketio.init_app(app, message_queue=REDIS_URL)
jwt = JWTManager(app)
app.debug = True
toolbar = DebugToolbarExtension(app)

#login manager

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'site.login'

@app.before_request
def make_session_permanent():
    session.permanent = True
    permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE_TIME)
    session.modified = True

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
from flask_restful import Api

@app.errorhandler(400)
def custom_401(error):
    return render_template('site/400.html'), 400
    # return Response('دسترسی شما به آدرس مورد نظر ممکن نیست', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})

# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

api = Api(app,'/api')

api.add_resource(Auth_API.UserRegistration,'/register')
api.add_resource(Auth_API.UserLogin, '/login')
# api.add_resource(Auth_API.UserLogout, '/logout')

api.add_resource(Site_API.SiteCategoryMenuItems, '/site/category/menu/items')
api.add_resource(Site_API.SiteCategoryAuctions, '/site/category/<int:cid>/auctions/')
api.add_resource(Site_API.SiteCategoryProducts, '/site/category/<int:cid>/products/')
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
api.add_resource(Auction_API.AuctionViewFinished, '/auction/view/finished')


api.add_resource(User_API.PaymentsInfo, '/user/payments/info/<int:pagenum>/<int:pagesize>')
api.add_resource(User_API.UserInformation, '/user/information')
api.add_resource(User_API.UserContactUs, '/user/contactus')
# api.add_resource(websocket.Join, '/join/<int:auction_id')
