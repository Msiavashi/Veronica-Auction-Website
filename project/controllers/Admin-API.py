
from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
# from project.model.user import User
from project.logger import Logger


# Routes
class AdminView(FlaskView):
    trailing_slash = False 
    route_prefix = '/api/'
    

    @route('/category/<int:cid>/product/<int:pid>', methods=['GET'])
    def product_details(self, cid, pid):
        pass
        


AdminView.register(app)



