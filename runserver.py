#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app
from project.database import init_db
import project.rest_generator




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run('0.0.0.0', port=port)