from sqlalchemy import Column, String
from flask_sqlalchemy import SQLAlchemy
from src.enums import Permission 
from sqlalchemy.ext.declarative import declarative_base
from src.utils.generate_uuid import generate_uuid

Base = declarative_base()
db = SQLAlchemy()

class User(Base):
    __tablename__ = "user"

    id = Column(String(), primary_key=True, default=generate_uuid)
    email = Column(String(), unique=True, nullable=False) 
    password = Column(String)
    position_id = Column(String)

class Role_permission(db.Model):
    __tablename__ = "role_permission"

    user_id = db.Column(db.String(), primary_key=True, nullable=False)
    permission = db.Column(db.Enum(Permission), unique=False, nullable=False)

class Position(Base):
    __tablename__ = "position"

    id = Column(String(), primary_key=True, default=generate_uuid)
    title = Column(String(), nullable=False) 