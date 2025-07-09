from sqlalchemy import String, Integer, Text, Column,  func, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    phone_number = Column(String(20), unique=True, index=True)
    password = Column(Text, nullable=True)
    code = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())