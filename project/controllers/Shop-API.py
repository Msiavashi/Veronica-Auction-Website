from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
# from project.model.user import User
from project.model.category import Category
from project.model.product import Product
from project.logger import Logger
from project.model.offer import Offer
import json

# Routes
class ShopView(FlaskView):
    trailing_slash = False
    route_prefix = '/api/'

    def index(self):
        return "this is index of shop api"


    @route("/category/<int:cid>/products", methods=['GET'])
    def products(self, cid):
        products = Product.query.filter_by(category_id=cid).count()
        return jsonify({"count":products}),200

    @route("/sildebar", methods=['GET'])
    def slidebar(self):
        pass


    @route("/offers", methods=['GET'])
    def offs(self):
        offers = Offer.query.count()
        if offers:
            return jsonify(offers=offers) , 200
        return jsonify({"mdg":"not any offer founded"}), 401


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
        categories = Category.query.all()
        if categories:
            jsonStr = json.dumps([i.to_json for i in categories])
            return jsonStr , 200
        return jsonify({"msg":"not any categories founded"}), 401

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
