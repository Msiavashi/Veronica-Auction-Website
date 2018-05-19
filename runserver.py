#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app
from project.database import init_db
from project.admin import admin
import definitions

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run('0.0.0.0', port=port)
