
from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
from project.logger import Logger


# Routes
class UserView(FlaskView):
    trailing_slash = False 
    route_prefix = '/api/'
    
    @route('/user/<int:uid>/product/<int:pid>/comment', methods=['POST'])
    def comment(self, uid, pid):
        pass
        
    @route('/user/<int:uid>', methods=['GET'])
    def user_info(self, uid):
        pass
        
    @route('/user/<int:uid>/auctions', methods=['GET'])
    def auctions(self, uid):
        pass
        
    @route('/user/<int:uid>/auction/<int:aid>/bid', methods=['POST'])
    def bid(self, uid, aid):
        pass
        
    @route('/user/<int:uid>/auction/<int:aid>', methods=['POST'])
    def auction_register(self, uid, aid):
        pass
        
    @route('/user/<int:uid>/auction/<int:aid>', methods=['PATCH'])
    def auction_edit(self, uid, aid):
        pass
        
    @route('/user/<int:uid>/auction/<int:aid>', methods=['DELETE'])
    def auction_delete(self, uid, aid):
        pass
        
    @route('/user/<int:uid>/auction', methods=['GET'])
    def auction_create(self, uid):
        pass
        

UserView.register(app)



