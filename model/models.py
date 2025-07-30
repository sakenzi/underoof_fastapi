from sqlalchemy import String, Integer, Text, Column, func, DateTime, ForeignKey, Float, Boolean, DECIMAL, Date
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True, unique=True)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True)
    password = Column(String, nullable=True)
    verification_code = Column(String(6), nullable=True) 
    is_active = Column(Boolean, default=False)

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
    advertisements = relationship("Advertisement", back_populates="user_role")


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
    advertisements = relationship("Advertisement", back_populates="location")


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    photo_link = Column(Text, nullable=False)

    advertisement_photos = relationship("AdvertisementPhoto", back_populates="photo")


class TypeAdvertisement(Base):
    __tablename__ = 'type_advertisements'

    id = Column(Integer, primary_key=True)
    type_name = Column(String, nullable=False)

    advertisements = relationship("Advertisement", back_populates="type_advertisement")


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    number_of_room = Column(Integer, nullable=True)
    quadrature = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    price = Column(Integer, nullable=False)
    from_the_date = Column(Date, nullable=False)
    before_the_date = Column(Date, nullable=False)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    type_advertisement_id = Column(Integer, ForeignKey("type_advertisements.id"), nullable=False)
    user_role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)

    location = relationship("Location", back_populates="advertisements")
    type_advertisement = relationship("TypeAdvertisement", back_populates="advertisements")
    user_role = relationship("UserRole", back_populates="advertisements")
    advertisement_photos = relationship("AdvertisementPhoto", back_populates="advertisement")


class AdvertisementPhoto(Base):
    __tablename__ = 'advertisement_photos'

    id = Column(Integer, primary_key=True)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)

    photo = relationship("Photo", back_populates="advertisement_photos")
    advertisement = relationship("Advertisement", back_populates="advertisement_photos")