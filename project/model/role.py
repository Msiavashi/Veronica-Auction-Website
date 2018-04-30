import datetime
from project.database import Base, db
# from project.model.customer import Customer


class Role(Base):
    __tablename__ = 'role'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(512))
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id'))