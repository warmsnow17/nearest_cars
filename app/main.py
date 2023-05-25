import asyncio

from fastapi import FastAPI
import uvicorn
import string
import random
from typing import Tuple

import pandas as pd
from sqlalchemy import make_url, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.database import create_pool
from app.models import Location, Truck

app = FastAPI()

from sqlalchemy.exc import IntegrityError


@app.on_event("startup")
async def startup_event():

    pool = create_pool()
    async with pool() as db:
        await create_locations(db)
        await create_trucks(db)


async def create_locations(db: AsyncSession):
    df = pd.read_csv('../uszips.csv')

    df = df[['zip', 'lat', 'lng', 'city', 'state_id']]

    df = df.head(100)

    data = df.to_dict('records')

    for row in data:
        location = Location(
            city=row['city'],
            state=row['state_id'],
            zip_code=row['zip'],
            latitude=row['lat'],
            longitude=row['lng'],
        )

        try:
            db.add(location)
            await db.flush()
        except IntegrityError:
            await db.rollback()
            print(f"Location {location.zip_code} already exists in the database. Skipping...")

    await db.commit()


def generate_unique_number():
    return str(random.randint(1000, 9999)) + random.choice(string.ascii_uppercase)


async def create_trucks(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Location))
        locations = result.scalars().all()

    for _ in range(20):
        location = random.choice(locations)
        unique_number = generate_unique_number()
        truck = Truck(
            unique_number=unique_number,
            current_location=location.city,
            load_capacity=random.randint(1, 1000)
        )
        db.add(truck)
        await db.commit()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
