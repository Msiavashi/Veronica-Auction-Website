#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, socketio
from project.database import *
from project.admin import admin

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    # app.run('0.0.0.0', port=port, threaded=True)
    socketio.run(app, port=port, debug=True)
    #for test commit
