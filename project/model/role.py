from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean
from sqlalchemy.types import BigInteger, TIMESTAMP
from sqlalchemy.orm import relationship, backref
import datetime
from user_role import user_roles
from project.database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(512))
    users = relationship('User', secondary=user_roles,back_populates='roles')
