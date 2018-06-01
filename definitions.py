# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Project Root
STATIC_DIR = os.path.join(ROOT_DIR, "project/static/")
AVATAR_DIR = os.path.join(ROOT_DIR, "project/static/images/avatars")
BASE_BID_PRICE = 1000
SESSION_EXPIRE_TIME = 100
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'messages', 'attachments')
ALLOWED_EXTENTIONS = set(['text', 'pdf', 'doc', 'docs', 'jpg', 'jpeg', 'png'])
MESSAGE_SUBJECTS = [{"title":'درخواست کمک','type':1},{"title":'مشکل در سایت','type':2},{"title":'تقدیر و تشکر','type':3}]
MAXIMUM_ORDERS = 3
