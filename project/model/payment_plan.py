from project.database import db, Base

payment_plans = db.Table('payment_plans', Base.metadata,
    db.Column('payment_id', db.ForeignKey('payments.id')),
    db.Column('plan_id', db.ForeignKey('plans.id'))
)
