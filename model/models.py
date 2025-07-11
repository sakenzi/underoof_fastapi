from sqlalchemy import String, Integer, Text, Column, func, DateTime, ForeignKey, Float, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(20), unique=True, index=True)
    password = Column(String, nullable=False)

    user_roles = relationship("UserRole", back_populates="user")


class PhoneCode(Base):
    __tablename__ = 'phone_codes'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, index=True)
    code = Column(String(10), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(20), unique=True, index=True)

    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False, index=True)

    streets = relationship("Street", back_populates="city")


class Street(Base):
    __tablename__ = 'streets'

    id = Column(Integer, primary_key=True)
    street_name = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey('cities.id'), nullable=True)

    city = relationship("City", back_populates="streets")
    locations = relationship("Location", back_populates="street")


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)

    street_id = Column(Integer, ForeignKey('streets.id'), nullable=True)

    street = relationship("Street", back_populates="locations")