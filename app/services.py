from typing import Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.models import Cargo, Truck, Location
from geopy.distance import geodesic


def calculate_distance(location1: Tuple[float, float], location2: Tuple[float, float]) -> float:
    return geodesic(location1, location2).miles


async def get_all_cargos_and_trucks(db: AsyncSession):
    cargos = await db.execute(
        select(Cargo).options(joinedload(Cargo.pick_up_location), joinedload(Cargo.delivery_location)))
    cargos = cargos.scalars().all()
    trucks = await db.execute(select(Truck).options(joinedload(Truck.current_location)))
    trucks = trucks.scalars().all()

    if not cargos:
        raise HTTPException(status_code=404, detail="No cargos found")

    if not trucks:
        raise HTTPException(status_code=404, detail="No trucks found")

    return cargos, trucks


async def get_cargo_and_trucks_by_id(db: AsyncSession, cargo_id: int):
    result = await db.execute(
        select(Cargo).options(joinedload(Cargo.pick_up_location), joinedload(Cargo.delivery_location)).where(
            Cargo.id == cargo_id)
    )
    cargo = result.scalar()
    if not cargo:
        raise HTTPException(status_code=404, detail=f"Cargo not found with id {cargo_id}")
    trucks_result = await db.execute(select(Truck).options(joinedload(Truck.current_location)))
    trucks = trucks_result.scalars().all()

    return cargo, trucks


async def get_truck_and_new_location_by_id(db: AsyncSession, truck_id: int, zip_code: int):
    result = await db.execute(select(Truck).where(Truck.id == truck_id))
    truck = result.scalar()
    result = await db.execute(select(Location).where(Location.zip_code == zip_code))
    new_location = result.scalar()

    if not truck:
        raise HTTPException(status_code=404, detail=f"No truck found with id {truck_id}")

    if not new_location:
        raise HTTPException(status_code=404, detail=f"No location found with zip code {zip_code}")

    return truck, new_location
