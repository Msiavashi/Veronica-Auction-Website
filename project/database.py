
from flask_sqlalchemy import SQLAlchemy
from project.db_config import Config
from project import app
from sqlalchemy.ext.declarative import declarative_base

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
db = SQLAlchemy(app)
Base = db.Model


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import project.model
    db.create_all()

# print "initing..."
# init_db()
# print "done"