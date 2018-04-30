from sqlalchemy import Integer, Column, Text, ForeignKey, String, Boolean, Table
from sqlalchemy.types import BigInteger, TIMESTAMP, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from project.database import Base

user_roles = Table('user_roles', Base.metadata,
    Column('role_id', ForeignKey('roles.id')),
    Column('user_id', ForeignKey('users.id'))
)
