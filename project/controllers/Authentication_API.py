from project import app
from project.database import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
from project.model.user import User
from project.logger import Logger


# Routes

class Authentication(FlaskView):
    trailing_slash = False
    route_prefix = '/api/'

    @route('/register/', methods=['POST'])
    def registration(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
        data = request.json
        print "data", data

        user = User()
        user.username = request.json.get('username',None)       #TODO: hash the password
        user.password = request.json.get('password',None)
        user.mobile = request.json.get('mobile',None)

        try:
            db.session.add(user)
            db.session.commit()
            #TODO: redirect and provide JWT token and return it
            return jsonify(success=True), 201
        except Exception as e:
            db.session.rollback()
            Logger.debug("registration: Could not add new user to database")
            Logger.error(e.message)
            return jsonify(success=False,message=e.message), 400

    @route('/login/', methods=['POST'])
    def login(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request","req":request.json}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        try:
            user = User.query.filter_by(username=username, password=password).first()
            if not user:
                return jsonify({"msg": "wrong username or password"}), 401

            #generating access token
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

        except Exception as e:
            Logger.debug("login: user could not login, entered username: " + username)
            Logger.error(e.message)
            print e.message
            return jsonify(success=False, message=e.message), 500


Authentication.register(app)
