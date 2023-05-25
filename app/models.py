from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cargo(Base):
    """Модель содержит информацию о грузе."""

    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True)
    pick_up_location = Column(String)
    delivery_location = Column(String)
    weight = Column(Integer)  # Диапазон веса должен быть проверен на уровне приложения.
    description = Column(String)


class Truck(Base):
    """Модель содержит информацию о грузовике."""

    __tablename__ = 'truck'

    id = Column(Integer, primary_key=True)
    unique_number = Column(String)
    current_location = Column(String)
    load_capacity = Column(Integer)  # Грузоподъемность должна быть проверена на уровне приложения.


class Location(Base):
    """Модель содержит информацию о локации."""

    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
