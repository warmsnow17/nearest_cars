import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Location, Truck
from sqlalchemy.exc import IntegrityError
import random
import string
import os


def generate_unique_number():
    return str(random.randint(1000, 9999)) + random.choice(string.ascii_uppercase)


async def create_locations(db: AsyncSession):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'uszips.csv')
    df = pd.read_csv(file_path)

    df = df[['zip', 'lat', 'lng', 'city', 'state_id']]

    df = df.head(5000)

    data = df.to_dict('records')

    async with db.begin():
        result = await db.execute(select(Location))
        locations = result.scalars().all()

        if len(locations) >= 5000:
            print("5000 or more locations already exist in the database. Skipping...")
            return

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


async def create_trucks(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Truck))
        trucks = result.scalars().all()

        if trucks:
            print("Trucks already exist in the database. Skipping...")
            return

        result = await db.execute(select(Location))
        locations = result.scalars().all()

    for _ in range(20):
        location = random.choice(locations)
        unique_number = generate_unique_number()
        truck = Truck(
            unique_number=unique_number,
            current_location=location,
            load_capacity=random.randint(1, 1000)
        )
        db.add(truck)
        await db.commit()
