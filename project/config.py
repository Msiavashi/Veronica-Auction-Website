from project.db_config import Config
import os

# Create dummy secrey key so we can use sessions
SECRET_KEY = os.urandom(32)
JWT_SECRET_KEY = os.urandom(32)
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Create in-memory database

<<<<<<< HEAD
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgres://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
=======
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
>>>>>>> 2a07f127a9c287e4a9ad8297ba2c38ab90ccc910
SQLALCHEMY_ECHO = True

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
