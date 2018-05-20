from project.db_config import Config
import os
import definitions

# Create dummy secrey key so we can use sessions
SECRET_KEY = os.urandom(32)
JWT_SECRET_KEY = os.urandom(32)
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Create in-memory database

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
SQLALCHEMY_ECHO = True

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Configure application to store JWTs in cookies. Whenever you make
# a request to a protected endpoint, you will need to send in the
# access or refresh JWT via a cookie.
JWT_TOKEN_LOCATION = 'cookies'

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
JWT_ACCESS_COOKIE_PATH = '/api/'
JWT_REFRESH_COOKIE_PATH = '/token/refresh'

# Disable CSRF protection for this example. In almost every case,
# this is a bad idea. See examples/csrf_protection_with_cookies.py
# for how safely store JWTs in cookies
JWT_COOKIE_CSRF_PROTECT = False

# CACHE_TYPE = 'simple'

# UPLOAD ATACHMENTS
UPLOAD_FOLDER = definitions.UPLOAD_FOLDER