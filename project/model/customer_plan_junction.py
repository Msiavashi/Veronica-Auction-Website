from project.database import Base, db

customer_plan_junction = db.Table('customer_plan_junction', 
    db.Column('customer_id', db.ForeignKey('customer.id')),
    db.Column('plan_id', db.ForeignKey('plan.id'))
)