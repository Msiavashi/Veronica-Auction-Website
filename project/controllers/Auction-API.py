
from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
# from project.model.user import User
from project.logger import Logger


# Routes
class AuctionView(FlaskView):
    trailing_slash = False 
    route_prefix = '/api/'
    

    @route('/auction/<int:aid>', methods=['GET'])
    def auction(self, aid):
        pass

    @route('/auction/newests', methods=['GET'])
    def newests(self):
        pass

    @route('/auction/slidebar', methods=['GET'])
    def slidebar(self):
        pass

    @route('/auction/histories', methods=['GET'])
    def histories(self):
        pass

    @route('/user/<int:uid>/auction/<int:aid>/running/websocket', methods=['GET'])
    def websocket(self, uid, aid):
        pass


AuctionView.register(app)



