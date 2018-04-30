from news_schema import news
from product_schema import product
from category_schema import category
from user_schema import UserSchema

users_schema = UserSchema(many=True)
# users_schema

category_schema = category()
categories_schema = category(many=True)

product_schema = product()
products_schema = product(many=True)

new_schema = news()
news_schema = news(many=True)
