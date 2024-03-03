from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=True)
    password_hash = Column(String)
    is_admin = Column(Boolean)
    # disabled = Column(Boolean)