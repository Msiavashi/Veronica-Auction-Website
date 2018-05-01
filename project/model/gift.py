from project.database import db, Base
from user_gift import user_gifts

class Gift(Base):
    __tablename__ = 'gifts'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=True)
    users = db.relationship('User', secondary=user_gifts, back_populates='gifts')
