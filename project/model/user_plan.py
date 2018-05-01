from project.database import db, Base

user_plans = db.Table('user_plans', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('plan_id', db.ForeignKey('plans.id')),
    db.Column('used',db.Boolean,default=False)
)
