# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Project Root
STATIC_DIR = os.path.join(ROOT_DIR, "project/static/")
AVATAR_DIR = os.path.join(ROOT_DIR, "project/files/avatars")
BASE_BID_PRICE = 1000
BASE_USER_CREDIT = 10000
SESSION_EXPIRE_TIME = 300
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'messages', 'attachments')
ALLOWED_EXTENTIONS = set(['text', 'pdf', 'doc', 'docs', 'jpg', 'jpeg', 'png'])
MESSAGE_SUBJECTS = [{"title":'درخواست کمک','type':1},{"title":'مشکل در سایت','type':2},{"title":'تقدیر و تشکر','type':3}]

#bank
BANK_MELLAT_TERMINAL_ID = 3556904
BANK_MELLAT_USERNAME = "bid2172"
BANK_MELLAT_PASSWORD = 49413744
MAXIMUM_ORDERS = 3
MAX_SEARCH_RESULT = 10
COUPONCODE = "ipuw-01mljeifb090[1n24p9[kjnqk]]"

SMS_SERVICE_NUMBER = '500010601642'
SMS_USERNAME = '09017414372'
SMS_PASSWORD = '3469'

MAX_ACTIVATION_ATTEMPTS = 3
MAX_LOGIN_ATTEMPTS = 20
MAX_MESSAGES_SEND = 5
MAX_DEFFER_ACTIVATION_TIME = 30 * 60
MAX_AVAILABLE_MESSAGE_TIME = 120
MAX_INVITOR_POLICY = 5
