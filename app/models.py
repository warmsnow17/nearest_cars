from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cargo(Base):
    """Модель содержит информацию о грузе."""

    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True)
    pick_up_location_id = Column(Integer, ForeignKey('location.id'))
    delivery_location_id = Column(Integer, ForeignKey('location.id'))
    weight = Column(Integer)
    description = Column(String)
    pick_up_location = relationship('Location', foreign_keys=[pick_up_location_id])
    delivery_location = relationship('Location', foreign_keys=[delivery_location_id])


class Truck(Base):
    """Модель содержит информацию о грузовике."""

    __tablename__ = 'truck'

    id = Column(Integer, primary_key=True)
    unique_number = Column(String)
    current_location_id = Column(Integer, ForeignKey('location.id'))
    load_capacity = Column(Integer)
    current_location = relationship('Location', foreign_keys=[current_location_id])


class Location(Base):
    """Модель содержит информацию о локации."""

    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
