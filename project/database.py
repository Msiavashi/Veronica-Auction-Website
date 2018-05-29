from flask_sqlalchemy import SQLAlchemy
from . import app
from sqlalchemy.ext.declarative import declarative_base
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


db = SQLAlchemy(app)
Base = db.Model

def init_db():
    from . import model
    # db.drop_all()
    db.create_all()

# print "initing..."
# init_db()
# print "done"

def migrate():
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    from . import model
    manager.run()

# print "migrating ... "
#migrate()
# print "migration done..!"
