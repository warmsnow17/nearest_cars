from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Cargo, Location
from app.schemas import (CargoCreate, CargoDetailOut, CargoListOut, CargoOut,
                         CargoUpdate, CargoUpdateListOut, TruckDistance,
                         TruckUpdate)
from app.services import get_all_cargos_and_trucks, calculate_distance, get_cargo_and_trucks_by_id, \
    get_truck_and_new_location_by_id

router = APIRouter()


@router.post("/cargo/", response_model=CargoOut)
async def create_cargo(cargo: CargoCreate, db: AsyncSession = Depends(get_db)):
    pick_up_location = await db.execute(select(Location).where(Location.zip_code == cargo.pick_up_location))
    delivery_location = await db.execute(select(Location).where(Location.zip_code == cargo.delivery_location))
    pick_up_location = pick_up_location.scalars().first()
    delivery_location = delivery_location.scalars().first()
    if not pick_up_location or not delivery_location:
        raise HTTPException(status_code=404, detail="Location not found")
    new_cargo = Cargo(
        pick_up_location_id=pick_up_location.id,
        delivery_location_id=delivery_location.id,
        weight=cargo.weight,
        description=cargo.description
    )
    db.add(new_cargo)
    await db.commit()
    return CargoOut(
        id=new_cargo.id,
        pick_up_location=pick_up_location.city,
        delivery_location=delivery_location.city,
        weight=new_cargo.weight,
        description=new_cargo.description
    )


@router.get("/cargos", response_model=List[CargoListOut])
async def get_cargos_with_nearest_trucks(db: AsyncSession = Depends(get_db)):
    cargos, trucks = await get_all_cargos_and_trucks(db)
    cargo_outputs = []
    for cargo in cargos:
        try:
            pick_up_location_coords = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

            nearest_trucks_count = 0
            for truck in trucks:
                truck_location_coords = (truck.current_location.latitude, truck.current_location.longitude)

                pick_up_distance = calculate_distance(pick_up_location_coords, truck_location_coords)

                if pick_up_distance <= 450:
                    nearest_trucks_count += 1

            cargo_output = CargoListOut(
                id=cargo.id,
                pick_up_location=cargo.pick_up_location.city,
                delivery_location=cargo.delivery_location.city,
                nearest_trucks_count=nearest_trucks_count,
            )
            cargo_outputs.append(cargo_output)
        except Exception as e:
            print(f"Error occurred: {e}")

    return cargo_outputs


@router.get("/cargos/{cargo_id}", response_model=CargoDetailOut)
async def get_cargo_by_id(cargo_id: int, db: AsyncSession = Depends(get_db)):
    cargo, trucks = await get_cargo_and_trucks_by_id(db, cargo_id)
    pick_up_location_coords = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

    all_trucks = []
    for truck in trucks:
        truck_location_coords = (truck.current_location.latitude, truck.current_location.longitude)
        pick_up_distance = calculate_distance(pick_up_location_coords, truck_location_coords)
        all_trucks.append(TruckDistance(unique_number=truck.unique_number, distance=pick_up_distance))

    cargo_output = CargoDetailOut(
        id=cargo.id,
        pick_up_location=cargo.pick_up_location.city,
        delivery_location=cargo.delivery_location.city,
        weight=cargo.weight,
        description=cargo.description,
        all_trucks=all_trucks
    )

    return cargo_output


@router.patch("/trucks/{truck_id}")
async def update_truck(truck_id: int, truck_data: TruckUpdate, db: AsyncSession = Depends(get_db)):
    truck, new_location = await get_truck_and_new_location_by_id(db, truck_id, truck_data.zip_code)

    truck.current_location = new_location
    await db.commit()

    return {"message": "Truck updated successfully"}


@router.patch("/cargos/{cargo_id}", response_model=CargoUpdateListOut)
async def update_cargo(cargo_id: int, cargo_update: CargoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cargo).where(Cargo.id == cargo_id))
    cargo = result.scalar()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    if cargo_update.weight is not None:
        cargo.weight = cargo_update.weight
    if cargo_update.description is not None:
        cargo.description = cargo_update.description

    await db.commit()

    cargo_output = CargoUpdateListOut(
        id=cargo.id,
        weight=cargo.weight,
        description=cargo.description
    )
    return cargo_output


@router.delete("/cargos/{cargo_id}")
async def delete_cargo(cargo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cargo).where(Cargo.id == cargo_id))
    cargo = result.scalar()

    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")

    await db.delete(cargo)
    await db.commit()

    return {"message": "Cargo has been deleted successfully"}
