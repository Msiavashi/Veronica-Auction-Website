#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, socketio
from project.database import *
from project.admin import admin

if __name__ == '__main__':
    # production
    port = int(os.environ.get("PORT", 8000))
    app.debug = False
    socketio.run(app, port=port, debug=False)

    # developement
    # port = int(os.environ.get("PORT", 9000))
    # app.debug = True
    # socketio.run(app, port=port, debug=True)
