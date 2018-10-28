from project.db_config import Config
import os
import definitions

# Create dummy secrey key so we can use sessions
# SECRET_KEY = "1qsj59$80__+j3o0-1cn.f=20-=@$&mp=-d1hkpwqhf2-==123ehdwoh^2n-^$@8-jf[=2ufiofh]"
# JWT_SECRET_KEY = "=921nlkwendq-019-4=1%@$-igj2f-=@FF2jpw00-=02=fjng809=292fj-209r=548@$Gdjp="
SECRET_KEY = os.urandom(124)
JWT_SECRET_KEY = os.urandom(124)
DEBUG_TB_INTERCEPT_REDIRECTS = False
# SESSION_TYPE = 'filesystem'

# Create in-memory database

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = Config.engine + '://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
SQLALCHEMY_ECHO = False
# SQLALCHEMY_MAX_CLIENT_CONN = 500
#
SQLALCHEMY_POOL_SIZE = 1000000
# SQLALCHEMY_POOL_RECYCLE = 3600
# SQLALCHEMY_MAX_OVERFLOW = 1000
# SQLALCHEMY_POOL_TIMEOUT = 30


JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_COOKIE_CSRF_PROTECT = False

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
JWT_REFRESH_COOKIE_PATH = '/api/'

# Disable CSRF protection for this example. In almost every case,
# this is a bad idea. See examples/csrf_protection_with_cookies.py
# for how safely store JWTs in cookies
# JWT_COOKIE_CSRF_PROTECT = False

# CACHE_TYPE = 'simple'

# UPLOAD ATACHMENTS
UPLOAD_FOLDER = definitions.UPLOAD_FOLDER
