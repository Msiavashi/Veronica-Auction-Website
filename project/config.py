from project.db_config import Config
import os

# Create dummy secrey key so we can use sessions
SECRET_KEY = os.urandom(32)
JWT_SECRET_KEY = os.urandom(32)
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Create in-memory database

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgres://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
SQLALCHEMY_ECHO = True

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
