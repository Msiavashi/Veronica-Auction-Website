from project.database import db, Base

user_roles = db.Table('user_roles', Base.metadata,
    db.Column('role_id', db.ForeignKey('roles.id')),
    db.Column('user_id', db.ForeignKey('users.id'))
)
