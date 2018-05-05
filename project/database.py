from flask_sqlalchemy import SQLAlchemy
from project import app
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy(app)
Base = db.Model

def init_db():
     import project.model
     #db.drop_all()
    #  db.create_all()

#print "initing..."
# init_db()
#print "done"
