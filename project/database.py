from flask_sqlalchemy import SQLAlchemy
from . import app
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy(app)
Base = db.Model

def init_db():
     from . import model
     #db.drop_all()
    #  db.create_all()

#print "initing..."
# init_db()
#print "done"
