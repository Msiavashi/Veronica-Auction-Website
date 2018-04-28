from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
# from project.model.user import User
from project.logger import Logger
from project.model.category import Category
from project.model.customer import Customer
# Routes
class ShopView(FlaskView):
    trailing_slash = False 
    route_prefix = '/api/'
    
    @route("/category/<int:cid>/products", methods=['GET'])
    def products(self, cid):
        pass

    @route("/sildebar", methods=['GET'])
    def slidebar(self):
        pass


    @route("/offs", methods=['GET'])
    def offs(self):
        pass

    @route("/advertisements", methods=['GET'])
    def advertisements(self):
        pass

    @route("/news", methods=['GET'])
    def news(self):
        pass

    @route("/user/<int:uid>/offers", methods=['GET'])
    def user_offers(self, uid):
        pass

    @route("/search", methods=['GET'])
    def search(self):

        pass
    @route("/categories", methods=['GET'])
    def categories(self):
        return Category.query.filter_by().first().id
        
    @route("/category/<int:cid>/bestseller/products", methods=['GET'])
    def products_best_seller(self):
        pass

    @route("/category/<int:cid>/mostliked/products", methods=['GET'])
    def products_most_liked(self):
        pass


    @route("/category/<int:cid>/newest/products", methods=['GET'])
    def products_newest(self):
        pass


    @route("/product/<int:pid>/comments", methods=['GET'])
    def comments(self):

        pass

            

ShopView.register(app)



