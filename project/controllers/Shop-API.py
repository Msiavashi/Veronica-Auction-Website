from project import app
from project.database import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_classy import FlaskView, route
from flask import jsonify, request
import datetime
from project.model.category import CategorySchema, Category
from project.model.product import *
from project.model.offer import *
from project.model.advertisement import *
from project.model.comment import *

# Routes
class ShopView(FlaskView):
    trailing_slash = False
    route_prefix = '/api/'

    @route("/category/<int:cid>/products", methods=['GET'])
    def products(self, cid):
        products = Product.query.filter_by(category_id=cid).all()
        product_schema = ProductSchema(many=True)
        return jsonify(product_schema.dump(products))

    @route("/slidebar", methods=['GET'])
    def slidebar(self):
        auction_ads = Advertisement.query.all()
        advertisement_schema = AdvertisementSchema(many=True)
        return jsonify(advertisement_schema.dump(auction_ads))


    @route("/offers", methods=['GET'])
    def offs(self):
        offer_schema = OfferSchema(many=True)
        return jsonify(offer_schema.dump(Offer.query.all()))


    @route("/advertisements", methods=['GET'])
    def advertisements(self):
        advertisement_schema = AdvertisementSchema(many=True)
        return jsonify(advertisement_schema.dump(Advertisement.query.all()))

    @route("/news", methods=['GET'])
    def news(self):
        pass

    @route("/user/<int:uid>/offers", methods=['GET'])
    def user_offers(self, uid):
        offer_schema = OfferSchema(many=True)
        return jsonify(offer_schema.dump(Offer.query.filter_by(user_id=uid)))

    @route("/search", methods=['GET'])
    def search(self):
        product_schema = ProductSchema(many=True)
        q = request.args.get('q')
        return jsonify(product_schema.dump(Product.query.filter(Product.name.like('%'+q+'%')).all()))

    @route("/categories", methods=['GET'])
    def categories(self):
        category_schema = CategorySchema(many=True)
        return jsonify(category_schema.dump(Category.query.all()))

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
    def comments(self,pid):
        comment_schema = CommentSchema(many=True)
        return jsonify(comment_schema.dump(Comment.query.filter_by(product_id=pid)))

    @route("/products", methods=['GET'])
    def products(self):
        product_schema = ProductSchema(many=True)
        return jsonify(product_schema.dump(Product.query.all()))


ShopView.register(app)
