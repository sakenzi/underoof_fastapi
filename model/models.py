from sqlalchemy import String, Integer, Text, Column, func, DateTime, ForeignKey, Float, Boolean, DECIMAL, Date, Index
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    surname = Column(String(100), nullable=True)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True)
    password = Column(String, nullable=True)
    verification_code = Column(String(6), nullable=True)
    verification_code_created_at = Column(DateTime(timezone=True), nullable=True)  
    is_active = Column(Boolean, default=False)

    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete", passive_deletes=True)
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete", passive_deletes=True)
    user_logos = relationship("UserLogo", back_populates="user", cascade="all, delete", passive_deletes=True)
    applications = relationship("Application", back_populates="user", cascade="all, delete", passive_deletes=True)


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

    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete", passive_deletes=True)


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")
    advertisements = relationship("Advertisement", back_populates="user_role", cascade="all, delete", passive_deletes=True)


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False, index=True)

    streets = relationship("Street", back_populates="city", cascade="all, delete", passive_deletes=True)


class Street(Base):
    __tablename__ = 'streets'

    id = Column(Integer, primary_key=True)
    street_name = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey('cities.id', ondelete="CASCADE"), nullable=True)

    city = relationship("City", back_populates="streets")
    locations = relationship("Location", back_populates="street", cascade="all, delete", passive_deletes=True)


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)

    street_id = Column(Integer, ForeignKey('streets.id', ondelete="CASCADE"), nullable=True)

    street = relationship("Street", back_populates="locations")
    advertisements = relationship("Advertisement", back_populates="location", cascade="all, delete", passive_deletes=True)


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    photo_link = Column(Text, nullable=False)

    advertisement_photos = relationship("AdvertisementPhoto", back_populates="photo", cascade="all, delete", passive_deletes=True)


class TypeAdvertisement(Base):
    __tablename__ = 'type_advertisements'

    id = Column(Integer, primary_key=True)
    type_name = Column(String, nullable=False)

    advertisements = relationship("Advertisement", back_populates="type_advertisement", cascade="all, delete", passive_deletes=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    number_of_room = Column(Integer, nullable=True)
    quadrature = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    price = Column(Integer, nullable=False)
    number_of_people = Column(Integer, nullable=True)
    from_the_date = Column(Date, nullable=False)
    before_the_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=True)
    type_advertisement_id = Column(Integer, ForeignKey("type_advertisements.id", ondelete="CASCADE"), nullable=False)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)

    location = relationship("Location", back_populates="advertisements")
    type_advertisement = relationship("TypeAdvertisement", back_populates="advertisements")
    user_role = relationship("UserRole", back_populates="advertisements")
    advertisement_photos = relationship("AdvertisementPhoto", back_populates="advertisement", cascade="all, delete", passive_deletes=True)
    favorites = relationship("Favorite", back_populates="advertisement", cascade="all, delete", passive_deletes=True)
    applications = relationship("Application", back_populates="advertisement", cascade="all, delete", passive_deletes=True)


class AdvertisementPhoto(Base):
    __tablename__ = 'advertisement_photos'

    id = Column(Integer, primary_key=True)
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id", ondelete="CASCADE"), nullable=False)

    photo = relationship("Photo", back_populates="advertisement_photos")
    advertisement = relationship("Advertisement", back_populates="advertisement_photos")


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey('advertisements.id', ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="favorites")
    advertisement = relationship("Advertisement", back_populates="favorites")


class Logo(Base):
    __tablename__ = 'logos'

    id = Column(Integer, primary_key=True)
    logo_link = Column(Text, nullable=False)

    user_logos = relationship("UserLogo", back_populates="logo", cascade="all, delete", passive_deletes=True)


class UserLogo(Base):
    __tablename__ = 'user_logos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    logo_id = Column(Integer, ForeignKey('logos.id', ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="user_logos")
    logo = relationship("Logo", back_populates="user_logos")


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    advertisement = relationship("Advertisement", back_populates="applications")
    user = relationship("User", back_populates="applications")
