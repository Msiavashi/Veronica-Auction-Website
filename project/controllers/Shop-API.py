from project import app
from project.database import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime

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
        user = Customer()
        user.first_name = "ahmad"
        user.last_name = "siavashi"
        user.username = "ahmads"
        user.password = "123456"
        user.email = "ahmads@gmail.com"
        user.phone_number = "2146798465"
        user.organization_or_person = "person"
        db.session.add(user)
        print (Customer.query.filter_by(username="ahmads").first().password)
        return "salam"
        # schema = CustomerSchema()
        # data = schema.dump(Customer.query.filter_by(username="ms95").first()).data
        # return data

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
