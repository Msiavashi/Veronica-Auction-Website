from flask_restless import APIManager
from project.database import db
from project.model import *
from project import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from project.controllers.Authentication_API import *

manager = APIManager(app, flask_sqlalchemy_db=db)



manager.create_api(Category, methods = ['GET'])
manager.create_api(Product, methods = ['GET'])

